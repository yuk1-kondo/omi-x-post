# -*- coding: utf-8 -*-
import asyncio
import re
from typing import Optional
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))  # Load .env file


class GeminiClient:
    """Gemini API client wrapper."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_text(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")
        response = self.model.generate_content(prompt)
        return (response.text or "").strip()


gemini_client = GeminiClient()


class TweetDetector:
    """Detects tweet trigger phrases and extracts tweet content."""
    
    TRIGGER_PHRASES = [
        "x now",
        "x\u30ca\u30a6",
        "x\u306a\u3046",
        "\u30a8\u30c3\u30af\u30b9\u30ca\u30a6",
        "\u30a8\u30c3\u30af\u30b9\u306a\u3046",
        "\u30a8\u30b9\u30ca",
        "\u3048\u3059\u306a",
        "\u30a8\u30b9\u30ca\u30a6",
        "\u3048\u3059\u306a\u3046",
        "\u30a8\u30af\u30b9\u30ca\u30a6",
        "\u30a8\u30af\u30b9\u306a\u3046",
        "\u3048\u304f\u3059\u306a\u3046",
        "tweet now",
        "post tweet",
        "send tweet",
        "tweet this",
        "post this tweet",
        "post to x"
    ]
    
    END_PHRASES = [
        "end tweet",
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
        
        if trigger_index == -1 or matched_trigger is None:
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
        
        # Very short tweets might still be complete
        cleaned = accumulated_text.strip().lstrip('.,!?;: ')
        if len(cleaned) < 3:
            return 0.0
        
        prompt = f"""You judge whether a short text sounds like a complete post.

    Complete (0.8-1.0):
    - A single thought/emotion feels finished
    - Can be posted as-is
    Examples:
    - "This is great" -> 0.9
    - "Best day ever" -> 0.95
    - "Love this" -> 0.9

    Incomplete (0.0-0.4):
    - The sentence is cut off
    - It clearly needs continuation
    Examples:
    - "I was thinking that" -> 0.2
    - "This is" -> 0.1
    - "Today was the best" -> 0.15

    If it sounds postable even if short, score 0.7 or higher.
    Output ONLY a number between 0.0 and 1.0.

    Text: "{cleaned}"
    Score:"""

        try:
            result = await asyncio.to_thread(gemini_client.generate_text, prompt)
            score = float(result.strip())
            score = max(0.0, min(1.0, score))
            print(f"INFO Completeness: {score:.2f} for '{cleaned[:50]}...'", flush=True)
            return score
        except Exception as e:
            print(f"WARN AI check failed: {e}, defaulting to complete", flush=True)
            return 0.9 if len(cleaned) > 8 else 0.5
    
    @classmethod
    async def ai_extract_tweet_from_segments(cls, all_segments_text: str) -> str:
        """
        Extract the actual tweet from 3 segments of speech.
        AI intelligently determines what's the tweet vs what's not.
        """
        prompt = f"""You extract the intended tweet from a voice transcript in Japanese.

    Assumption: The user said a trigger phrase and then kept talking.

    Rules:
    1. Extract only what should be posted
    2. Remove side remarks, false starts, or corrections
    3. Remove filler words (um, uh, like, you know, etc.)
    4. Fix grammar, punctuation, and capitalization
    5. If the sentence is cut off, complete it naturally (e.g., "\u5c31\u5bdd\u3059" -> "\u5c31\u5bdd\u3057\u307e\u3059")
    6. Keep it under 280 characters
    7. Always render "\u304a\u307f" or "\u30aa\u30df" as "Omi"

    Examples:
    Input: "\u4eca\u65e5\u306f\u3082\u3046\u5c31\u5bdd\u3059"
    Output: "\u4eca\u65e5\u306f\u3082\u3046\u5c31\u5bdd\u3057\u307e\u3059\u3002"

    Output ONLY the tweet text. No quotes or explanations.

    Transcript: {all_segments_text}
    Tweet:"""

        try:
            cleaned = await asyncio.to_thread(gemini_client.generate_text, prompt)
            cleaned = cleaned.strip()

            if cleaned.startswith('"') and cleaned.endswith('"'):
                cleaned = cleaned[1:-1]
            if cleaned.startswith("'") and cleaned.endswith("'"):
                cleaned = cleaned[1:-1]

            if cleaned and cleaned[0].islower():
                cleaned = cleaned[0].upper() + cleaned[1:]

            if len(cleaned) > 280:
                cleaned = cleaned[:277] + "..."

            return cleaned

        except Exception as e:
            print(f"WARN AI extraction failed: {e}, using basic cleanup", flush=True)
            return cls.clean_tweet_content(all_segments_text)
    
    @classmethod
    async def ai_clean_tweet(cls, full_text: str, extracted_content: str) -> str:
        """
        Use Gemini to clean and refine the tweet text.
        Takes the full transcript and extracted content, returns cleaned tweet.
        """
        prompt = f"""You are a tweet cleanup assistant.

    Your job:
    1. Make it a natural, readable tweet
    2. Remove filler words
    3. Fix grammar, punctuation, and capitalization
    4. Keep it under 280 characters
    5. Preserve the original meaning and tone
    6. Always render "\u304a\u307f" or "\u30aa\u30df" as "Omi"

    Output ONLY the cleaned tweet text.

    Full transcript: {full_text}
    Extracted content: {extracted_content}
    Tweet:"""

        try:
            cleaned = await asyncio.to_thread(gemini_client.generate_text, prompt)
            cleaned = cleaned.strip()

            if cleaned.startswith('"') and cleaned.endswith('"'):
                cleaned = cleaned[1:-1]
            if cleaned.startswith("'") and cleaned.endswith("'"):
                cleaned = cleaned[1:-1]

            if cleaned and cleaned[0].islower():
                cleaned = cleaned[0].upper() + cleaned[1:]

            if len(cleaned) > 280:
                cleaned = cleaned[:277] + "..."

            return cleaned

        except Exception as e:
            print(f"WARN AI cleanup failed: {e}, using basic cleanup")
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

