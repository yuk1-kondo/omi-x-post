# 🐦 OMI Twitter Integration

Voice-activated Twitter posting through your OMI device. Simply say "Tweet Now" followed by your message, and it will be automatically posted to Twitter!

## ✨ Features

- **Voice-Activated Tweeting**: Say "Tweet Now" and your message to post instantly
- **AI-Powered Tweet Detection**: Intelligent boundary detection knows when your tweet ends
- **One-Time Authentication**: Connect your Twitter account once, tweet forever
- **Real-Time Processing**: Processes your speech as you talk
- **Smart Content Cleaning**: Removes filler words and cleans up your tweet automatically

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Twitter Developer Account with API v2 access
- OpenAI API key
- OMI device and app

### 1. Twitter Developer Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app or use an existing one
3. Enable **OAuth 2.0**
4. Set the following OAuth 2.0 settings:
   - **Type of App**: Web App
   - **Callback URLs**: `http://localhost:8000/auth/callback` (or your deployed URL)
   - **Website URL**: Your app website or GitHub repo
5. Set permissions to **Read and Write**
6. Note down your:
   - API Key
   - API Key Secret
   - Client ID
   - Client Secret

### 2. OpenAI API Setup

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key (starts with `sk-...`)

### 3. Installation

```bash
# Clone or navigate to the project directory
cd /path/to/twitter

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_CLIENT_ID=your_client_id_here
TWITTER_CLIENT_SECRET=your_client_secret_here

# OAuth Redirect URL (must match Twitter app settings)
OAUTH_REDIRECT_URL=http://localhost:8000/auth/callback

# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-key-here

# Database
DATABASE_URL=sqlite+aiosqlite:///./twitter_omi.db

# App Settings
APP_HOST=0.0.0.0
APP_PORT=8000
```

### 5. Run the Application

```bash
# Make sure virtual environment is activated
python main.py
```

The app will start on `http://localhost:8000`

### 6. Deploy (Optional but Recommended)

For production use, deploy to a cloud service:

**Option A: Railway.app**
1. Create account at [Railway.app](https://railway.app)
2. Connect your GitHub repo
3. Add environment variables
4. Deploy

**Option B: Render.com**
1. Create account at [Render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Add environment variables
5. Deploy

**Option C: Heroku**
```bash
heroku create your-app-name
heroku config:set TWITTER_API_KEY=xxx ...
git push heroku main
```

**Important**: Update `OAUTH_REDIRECT_URL` in your `.env` and Twitter app settings to match your deployed URL.

### 7. Setup in OMI App

1. Open the OMI mobile app
2. Go to **Settings** → Enable **Developer Mode**
3. Go to **Developer Settings**
4. Create a new Integration App:
   - **App Name**: Twitter Voice Poster
   - **Description**: Post tweets with your voice
   - **App Type**: Real-Time Transcript Processor
   - **Webhook URL**: `http://your-domain:8000/webhook` (or your deployed URL)
   - **Setup Completed URL**: `http://your-domain:8000/setup-completed`
   - **Auth URL**: `http://your-domain:8000/auth`
   - **Setup Instructions**: Link to this README or custom instructions

5. Save and install the app
6. Click **Authenticate** to connect your Twitter account

## 📱 How to Use

### Basic Usage

1. Make sure the app is enabled in your OMI app
2. Start speaking to your OMI device
3. Say the trigger phrase: **"Tweet Now"**
4. Say your tweet content
5. The AI will automatically detect when you're done and post the tweet

### Examples

**Example 1: Simple Tweet**
```
"Tweet Now, Just had an amazing conversation about AI and creativity. The future is exciting!"
```

**Example 2: With Explicit End**
```
"Tweet Now, Working on a new project that combines voice AI with social media. This is going to be awesome. End tweet."
```

**Example 3: Natural Speech**
```
"Tweet Now, I think artificial intelligence is going to change how we interact with technology in ways we can't even imagine yet."
```

### Trigger Phrases

Any of these will start a tweet:
- "Tweet Now"
- "Post Tweet"
- "Send Tweet"
- "Tweet This"
- "Post This Tweet"

### Ending Tweets

The AI automatically detects when your tweet is complete, but you can also say:
- "End Tweet"
- "Stop Tweet"
- "That's It"
- "Done Tweeting"
- "Finish Tweet"

## 🔧 Configuration Options

### Tweet Detection Settings

Edit `tweet_detector.py` to customize:

```python
# Add custom trigger phrases
TRIGGER_PHRASES = [
    "tweet now",
    "post tweet",
    "your custom phrase"
]

# Add custom end phrases
END_PHRASES = [
    "end tweet",
    "your custom end phrase"
]
```

### AI Model

By default, the app uses `gpt-4o-mini` for tweet boundary detection. Change in `tweet_detector.py`:

```python
model="gpt-4o-mini"  # or "gpt-4o" for more accuracy
```

## 🧪 Testing

### Local Testing

1. Start the server:
```bash
python main.py
```

2. Test authentication:
```bash
# Visit in browser
http://localhost:8000/auth?uid=test_user_123
```

3. Test webhook with curl:
```bash
curl -X POST "http://localhost:8000/webhook?session_id=test123&uid=test_user_123" \
  -H "Content-Type: application/json" \
  -d '[{"text": "Tweet Now, This is a test tweet!", "speaker": "SPEAKER_00", "is_user": true, "start": 0, "end": 5}]'
```

### Test with OMI Device

1. Enable the app in OMI
2. Authenticate your Twitter account
3. Enable Developer Mode in OMI settings
4. Set your webhook URL in Developer Settings
5. Start speaking and test the trigger phrase

## 🐛 Troubleshooting

### Common Issues

**"User not authenticated" error**
- Make sure you've completed the OAuth flow
- Check that your Twitter credentials are correct
- Verify the `uid` parameter matches your OMI user ID

**Tweets not posting**
- Check Twitter API rate limits
- Verify your app has "Read and Write" permissions
- Check server logs for errors

**AI not detecting tweet end**
- Try using explicit end phrases like "End Tweet"
- Make sure OpenAI API key is valid
- Check if tweet content is too short (needs 20+ characters)

**OAuth redirect not working**
- Verify `OAUTH_REDIRECT_URL` matches Twitter app settings exactly
- Check for typos in environment variables
- Ensure your server is accessible from the internet (for production)

### Logs

Check application logs for debugging:
```bash
# The app prints detailed logs to console
python main.py
```

### Database Issues

Reset the database if needed:
```bash
rm twitter_omi.db
# Restart the app - it will create a new database
python main.py
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | App information and status |
| `/auth?uid=<uid>` | GET | Start OAuth flow |
| `/auth/callback` | GET | OAuth callback handler |
| `/setup-completed?uid=<uid>` | GET | Check if user is authenticated |
| `/webhook?session_id=<id>&uid=<uid>` | POST | Real-time transcript processor |
| `/health` | GET | Health check |

## 🔐 Security Notes

- Never commit `.env` file to version control
- Use environment variables for all secrets
- In production, use HTTPS for all endpoints
- Regularly rotate API keys
- Consider implementing rate limiting
- Store tokens securely (consider encryption for production)

## 🎯 Advanced Features

### Custom Tweet Templates

Modify the AI prompt in `tweet_detector.py` to add custom formatting:

```python
"content": """Format tweets with specific style:
- Use hashtags appropriately
- Add emojis based on sentiment
- Keep under 280 characters"""
```

### Multiple Accounts

The app supports multiple users automatically. Each OMI `uid` can authenticate their own Twitter account.

### Analytics

Add analytics by logging tweets to a separate table:

```python
class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    content = Column(Text)
    posted_at = Column(DateTime)
    tweet_id = Column(String)
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🆘 Support

- **Issues**: Open an issue on GitHub
- **OMI Docs**: [https://docs.omi.me](https://docs.omi.me)
- **Twitter API**: [Twitter Developer Docs](https://developer.twitter.com/en/docs)

## 🎉 Credits

Built for the OMI ecosystem. Special thanks to:
- OMI team for the amazing wearable AI platform
- Twitter API for social media integration
- OpenAI for intelligent text processing

---

**Made with ❤️ for the OMI community**

