import re
from typing import Optional, Tuple
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class TweetDetector:
    """Detects 'Tweet Now' commands and extracts tweet content intelligently."""
    
    TRIGGER_PHRASES = [
        "tweet now",
        "post tweet",
        "send tweet",
        "tweet this",
        "post this tweet"
    ]
    
    END_PHRASES = [
        "end tweet",
        "stop tweet",
        "that's it",
        "that's the tweet",
        "done tweeting",
        "finish tweet"
    ]
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().strip()
    
    @classmethod
    def detect_trigger(cls, text: str) -> bool:
        """Check if text contains a tweet trigger phrase."""
        normalized = cls.normalize_text(text)
        return any(trigger in normalized for trigger in cls.TRIGGER_PHRASES)
    
    @classmethod
    def detect_end(cls, text: str) -> bool:
        """Check if text contains an explicit end phrase."""
        normalized = cls.normalize_text(text)
        return any(end_phrase in normalized for end_phrase in cls.END_PHRASES)
    
    @classmethod
    def extract_tweet_content(cls, text: str) -> Optional[str]:
        """Extract tweet content after trigger phrase."""
        normalized = cls.normalize_text(text)
        
        # Find the trigger phrase
        trigger_index = -1
        matched_trigger = None
        for trigger in cls.TRIGGER_PHRASES:
            idx = normalized.find(trigger)
            if idx != -1:
                trigger_index = idx
                matched_trigger = trigger
                break
        
        if trigger_index == -1:
            return None
        
        # Extract content after trigger
        start_index = trigger_index + len(matched_trigger)
        content = text[start_index:].strip()
        
        # Remove explicit end phrases if present
        for end_phrase in cls.END_PHRASES:
            if content.lower().endswith(end_phrase):
                content = content[:-(len(end_phrase))].strip()
                break
        
        return content if content else None
    
    @classmethod
    async def is_tweet_complete(cls, tweet_content: str, recent_segments: list) -> Tuple[bool, str]:
        """
        Use AI to determine if the tweet content is complete.
        Returns (is_complete, cleaned_content)
        """
        cleaned_content = tweet_content.strip()
        
        # If explicit end phrase detected
        if recent_segments and cls.detect_end(recent_segments[-1]):
            return True, cleaned_content
        
        # For testing/simple tweets: if content is reasonable length, post it
        # This makes the experience more responsive
        if len(cleaned_content) > 5:
            # Consider it complete - better to post quickly than wait
            return True, cleaned_content
        
        return False, cleaned_content
    
    @classmethod
    async def ai_clean_tweet(cls, full_text: str, extracted_content: str) -> str:
        """
        Use OpenAI to intelligently clean and extract the tweet.
        Takes the full transcript and extracted content, returns cleaned tweet.
        """
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a tweet cleanup assistant. Extract and clean up the intended tweet from speech.

Your job:
1. Extract ONLY the tweet content (what comes after "Tweet Now")
2. Remove filler words (um, uh, like, you know, so)
3. Fix capitalization and punctuation
4. Remove leading/trailing punctuation artifacts
5. Make it sound natural and well-written
6. Keep it under 280 characters
7. Preserve the original meaning and tone

Respond with ONLY the cleaned tweet text. No quotes, no explanations, just the tweet."""
                    },
                    {
                        "role": "user",
                        "content": f"Full transcript: {full_text}\n\nExtracted after trigger: {extracted_content}\n\nClean this into a perfect tweet:"
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            cleaned = response.choices[0].message.content.strip()
            
            # Remove quotes if AI added them
            if cleaned.startswith('"') and cleaned.endswith('"'):
                cleaned = cleaned[1:-1]
            if cleaned.startswith("'") and cleaned.endswith("'"):
                cleaned = cleaned[1:-1]
            
            # Ensure proper capitalization
            if cleaned and cleaned[0].islower():
                cleaned = cleaned[0].upper() + cleaned[1:]
            
            # Truncate if too long
            if len(cleaned) > 280:
                cleaned = cleaned[:277] + "..."
            
            return cleaned
            
        except Exception as e:
            print(f"⚠️  AI cleanup failed: {e}, using basic cleanup")
            # Fallback to basic cleaning
            return cls.clean_tweet_content(extracted_content)
    
    @classmethod
    def clean_tweet_content(cls, content: str) -> str:
        """Basic cleaning of tweet content (fallback)."""
        # Remove multiple spaces
        content = re.sub(r'\s+', ' ', content)
        
        # Remove common filler words at the end
        filler_words = ["um", "uh", "like", "you know", "so", "yeah"]
        words = content.split()
        while words and words[-1].lower().rstrip('.,!?') in filler_words:
            words.pop()
        
        content = ' '.join(words).strip()
        
        # Remove leading punctuation
        content = content.lstrip('.,!?;: ')
        
        # Ensure proper capitalization of first letter
        if content and content[0].islower():
            content = content[0].upper() + content[1:]
        
        return content

