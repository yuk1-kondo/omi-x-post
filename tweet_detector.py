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
    async def ai_check_completeness(cls, accumulated_text: str) -> float:
        """
        Use AI to check if tweet sounds complete.
        Returns a score from 0.0 to 1.0:
        - 0.0 = definitely incomplete, wait for more
        - 1.0 = definitely complete, post now
        - 0.5+ = probably complete enough
        """
        # If explicit end phrase, it's complete
        if cls.detect_end(accumulated_text):
            return 1.0
        
        # Very short tweets are likely incomplete
        if len(accumulated_text.strip()) < 5:
            return 0.0
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You analyze speech to determine if a tweet is complete.

A tweet is COMPLETE (1.0) if:
- It expresses a full thought
- Has proper ending (not mid-sentence)
- Makes sense on its own
- Doesn't sound cut off

A tweet is INCOMPLETE (0.0) if:
- Ends mid-sentence or mid-word
- Trailing words suggest more coming ("and...", "but...", "also...")
- Sounds like speaker was interrupted
- Missing obvious conclusion

Return ONLY a single number: 0.0 (incomplete) to 1.0 (complete)
Examples:
- "This is amazing" → 1.0 (complete)
- "This is" → 0.0 (incomplete)
- "I think that" → 0.2 (likely incomplete)
- "Just had a great idea and" → 0.1 (clearly incomplete)"""
                    },
                    {
                        "role": "user",
                        "content": f"Tweet content: {accumulated_text}\n\nCompleteness score (0.0-1.0):"
                    }
                ],
                temperature=0.1,
                max_tokens=10
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse the score
            try:
                score = float(result)
                score = max(0.0, min(1.0, score))  # Clamp between 0 and 1
                print(f"🤖 AI completeness score: {score:.2f}", flush=True)
                return score
            except:
                # If can't parse, assume moderately complete
                return 0.6
                
        except Exception as e:
            print(f"⚠️  AI check failed: {e}, assuming complete", flush=True)
            # On error, assume complete if reasonable length
            return 1.0 if len(accumulated_text.strip()) > 10 else 0.3
    
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

