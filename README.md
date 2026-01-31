# OMI X Voice Posting

```bash
git clone https://github.com/aaravgarg/omi-twitter-app.git
```

Real-time X posting via OMI voice commands. The app collects voice transcript
segments, uses AI to clean the content, and posts the final tweet to X.

## Features

- **Voice-triggered posting** via OMI
- **3-segment collection** with AI extraction and cleanup
- **OAuth 2.0** X account authentication
- **Notification only on final post** to avoid spam
- **Ready for cloud hosting** (Railway/Render/Fly)

## How it works (OMI user flow)

1. Connect your X account via OAuth
2. Speak to OMI and say a trigger phrase (e.g., "Tweet now")
3. The app collects 3 segments
4. AI extracts the intended tweet and posts it to X

## Trigger phrases

- "Tweet now"
- "Post tweet"
- "Send tweet"
- "Tweet this"
- "Post to X"

## AI behavior (Gemini)

Gemini is used to:

1. Decide if a short segment is complete
2. Extract the intended tweet from multiple segments
3. Clean punctuation, grammar, and casing
4. Keep tweets under 280 characters

## Setup

### Requirements

- Python 3.10+
- X API credentials (developer.x.com)
- Gemini API key
- OMI app + voice command integration

### Install

```bash
git clone https://github.com/aaravgarg/omi-twitter-app.git
cd omi-twitter-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Environment variables

```env
# X API Credentials (developer.x.com)
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret

# OAuth Redirect URL
OAUTH_REDIRECT_URL=http://localhost:8000/auth/callback

# Gemini API Key
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-1.5-flash

# App Settings
APP_HOST=0.0.0.0
APP_PORT=8000
```

### Run locally

```bash
source venv/bin/activate
python main_simple.py
```

Open the test console at:

```text
http://localhost:8000/test
```

## Endpoints

| Endpoint | Method | Purpose |
| -------- | ------ | ------- |
| `/` | GET | Setup page |
| `/auth` | GET | Start OAuth |
| `/auth/callback` | GET | OAuth callback |
| `/setup-completed` | GET | Auth status check |
| `/webhook` | POST | Receive transcript segments |
| `/test` | GET | Test console |
| `/health` | GET | Health check |

## Deploy (Railway)

1. Push to GitHub
2. Deploy on Railway
3. Set environment variables
4. Update OAuth Redirect URL to your deployed domain

## License

MIT License
