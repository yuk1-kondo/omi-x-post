from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

from models import init_db, get_db, User, Session
from twitter_client import TwitterClient
from tweet_detector import TweetDetector

load_dotenv()

# Initialize services
twitter_client = TwitterClient()
tweet_detector = TweetDetector()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    await init_db()
    yield


app = FastAPI(
    title="OMI Twitter Integration",
    description="Real-time Twitter posting via OMI voice commands",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint with app information."""
    return {
        "app": "OMI Twitter Integration",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "auth": "/auth?uid=<user_id>",
            "webhook": "/webhook?session_id=<session>&uid=<user_id>",
            "setup_check": "/setup-completed?uid=<user_id>"
        }
    }


@app.get("/auth")
async def auth_start(uid: str = Query(..., description="User ID from OMI")):
    """
    Start OAuth flow for Twitter authentication.
    OMI will redirect users here with their uid parameter.
    """
    redirect_uri = os.getenv("OAUTH_REDIRECT_URL", "http://localhost:8000/auth/callback")
    
    try:
        auth_url, state = twitter_client.get_authorization_url(redirect_uri)
        
        # Store uid in state for callback (in production, use proper state management)
        # For now, we'll pass it as a query param in redirect_uri
        auth_url_with_uid = f"{auth_url}&state={uid}"
        
        return RedirectResponse(url=auth_url_with_uid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth initialization failed: {str(e)}")


@app.get("/auth/callback")
async def auth_callback(
    request: Request,
    state: str = Query(None),
    code: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Handle OAuth callback from Twitter."""
    if not code:
        return HTMLResponse(
            content="""
            <html>
                <body style="font-family: Arial; padding: 40px; text-align: center;">
                    <h2>❌ Authentication Failed</h2>
                    <p>Authorization code not received. Please try again.</p>
                </body>
            </html>
            """,
            status_code=400
        )
    
    uid = state  # uid passed as state
    redirect_uri = os.getenv("OAUTH_REDIRECT_URL", "http://localhost:8000/auth/callback")
    
    try:
        # Exchange code for access token
        full_url = str(request.url)
        token_data = twitter_client.get_access_token(full_url, redirect_uri)
        
        # Get or create user
        result = await db.execute(select(User).where(User.uid == uid))
        user = result.scalar_one_or_none()
        
        if user:
            user.access_token = token_data.get('access_token')
            user.refresh_token = token_data.get('refresh_token')
        else:
            user = User(
                uid=uid,
                access_token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token')
            )
            db.add(user)
        
        await db.commit()
        
        return HTMLResponse(
            content="""
            <html>
                <head>
                    <style>
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #1DA1F2 0%, #0d8bd9 100%);
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 16px;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                            text-align: center;
                            max-width: 400px;
                        }
                        .success-icon {
                            font-size: 64px;
                            margin-bottom: 20px;
                        }
                        h2 {
                            color: #1DA1F2;
                            margin-bottom: 10px;
                        }
                        p {
                            color: #666;
                            line-height: 1.6;
                        }
                        .instruction {
                            background: #f0f8ff;
                            padding: 20px;
                            border-radius: 8px;
                            margin-top: 20px;
                            border-left: 4px solid #1DA1F2;
                        }
                        .instruction strong {
                            color: #1DA1F2;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="success-icon">✅</div>
                        <h2>Successfully Connected!</h2>
                        <p>Your Twitter account is now linked to OMI.</p>
                        <div class="instruction">
                            <strong>How to use:</strong>
                            <p style="margin-top: 10px;">
                                Simply say <strong>"Tweet Now"</strong> followed by your message,
                                and it will be posted to Twitter automatically!
                            </p>
                            <p style="margin-top: 10px; font-size: 14px; color: #888;">
                                Example: "Tweet Now, Just had an amazing idea about AI and creativity!"
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
        )
    
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
                <body style="font-family: Arial; padding: 40px; text-align: center;">
                    <h2>❌ Authentication Error</h2>
                    <p>Failed to complete authentication: {str(e)}</p>
                    <p><a href="/auth?uid={uid}">Try again</a></p>
                </body>
            </html>
            """,
            status_code=500
        )


@app.get("/setup-completed")
async def check_setup(
    uid: str = Query(..., description="User ID from OMI"),
    db: AsyncSession = Depends(get_db)
):
    """
    Check if user has completed setup (authenticated with Twitter).
    Required by OMI integration spec.
    """
    result = await db.execute(select(User).where(User.uid == uid))
    user = result.scalar_one_or_none()
    
    is_setup = user is not None and user.access_token is not None
    
    return {"is_setup_completed": is_setup}


@app.post("/webhook")
async def webhook(
    request: Request,
    session_id: str = Query(..., description="Session ID from OMI"),
    uid: str = Query(..., description="User ID from OMI"),
    db: AsyncSession = Depends(get_db)
):
    """
    Real-time transcript webhook endpoint.
    Receives transcript segments and processes tweet commands.
    """
    # Get user
    result = await db.execute(select(User).where(User.uid == uid))
    user = result.scalar_one_or_none()
    
    if not user or not user.access_token:
        return JSONResponse(
            content={
                "message": "User not authenticated. Please complete setup first.",
                "setup_required": True
            },
            status_code=401
        )
    
    # Parse transcript segments
    try:
        segments: List[Dict[str, Any]] = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    
    if not segments or not isinstance(segments, list):
        return {"message": "No segments to process"}
    
    # Get or create session
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    session = result.scalar_one_or_none()
    
    if not session:
        session = Session(session_id=session_id, uid=uid)
        db.add(session)
        await db.commit()
        await db.refresh(session)
    
    # Process segments
    response_message = await process_segments(session, segments, user, db)
    
    return {
        "message": response_message,
        "session_id": session_id,
        "processed_segments": len(segments)
    }


async def process_segments(
    session: Session,
    segments: List[Dict[str, Any]],
    user: User,
    db: AsyncSession
) -> str:
    """Process transcript segments and handle tweet commands."""
    
    # Extract text from segments
    segment_texts = [seg.get("text", "") for seg in segments]
    full_text = " ".join(segment_texts)
    
    # State machine for tweet processing
    if session.tweet_mode == "idle":
        # Check for trigger phrase
        if tweet_detector.detect_trigger(full_text):
            # Extract initial tweet content
            tweet_content = tweet_detector.extract_tweet_content(full_text)
            
            if tweet_content:
                session.tweet_mode = "recording"
                session.tweet_content = tweet_content
                session.transcript = full_text
                await db.commit()
                
                return f"📝 Recording tweet: '{tweet_content}'"
            else:
                return "👂 Listening for your tweet..."
    
    elif session.tweet_mode == "recording":
        # Accumulate tweet content
        session.transcript += " " + full_text
        
        # Check if there's new content after the trigger
        if tweet_detector.detect_trigger(session.transcript):
            new_content = tweet_detector.extract_tweet_content(session.transcript)
            if new_content:
                session.tweet_content = new_content
        
        # Check if tweet is complete
        is_complete, cleaned_content = await tweet_detector.is_tweet_complete(
            session.tweet_content,
            segment_texts
        )
        
        if is_complete and len(cleaned_content.strip()) > 0:
            # Post tweet
            result = await twitter_client.post_tweet(user.access_token, cleaned_content)
            
            if result and result.get("success"):
                session.tweet_mode = "idle"
                session.tweet_content = ""
                session.transcript = ""
                await db.commit()
                
                return f"✅ Tweet posted: '{cleaned_content}'"
            else:
                error = result.get("error", "Unknown error") if result else "Failed to post"
                session.tweet_mode = "idle"
                await db.commit()
                
                return f"❌ Failed to post tweet: {error}"
        else:
            # Still recording
            await db.commit()
            return f"📝 Recording: '{session.tweet_content}...'"
    
    return "Listening..."


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "omi-twitter-integration"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8000))
    host = os.getenv("APP_HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )

