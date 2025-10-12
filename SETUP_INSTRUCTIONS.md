# 🐦 Twitter Voice Poster - Setup Instructions

## Quick Setup (5 minutes)

### Step 1: Get Twitter API Credentials

1. Visit [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Sign in with your Twitter account
3. Click **Create App** (or use existing app)
4. Fill in basic information:
   - **App Name**: Choose any name
   - **Description**: Voice-activated Twitter posting
   - **Website**: Your personal website or GitHub
5. Go to **App Settings** → **OAuth 2.0**
6. Enable OAuth 2.0 and set:
   - **Callback URL**: `http://your-domain:8000/auth/callback`
7. Set **App Permissions** to **Read and Write**
8. Save these credentials (you'll need them):
   - API Key
   - API Key Secret  
   - Client ID
   - Client Secret

### Step 2: Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key**
4. Copy the key (starts with `sk-...`)

### Step 3: Deploy the App

**Option A: Use the hosted version**
- Contact the developer for hosted endpoint URL
- Skip to Step 4

**Option B: Deploy yourself**
1. Fork/clone the repository
2. Deploy to [Railway](https://railway.app), [Render](https://render.com), or [Heroku](https://heroku.com)
3. Add environment variables:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_CLIENT_ID`
   - `TWITTER_CLIENT_SECRET`
   - `OPENAI_API_KEY`
   - `OAUTH_REDIRECT_URL` (your deployed URL + `/auth/callback`)
4. Note your deployed URL

### Step 4: Authenticate Your Twitter Account

1. Click the **Authenticate** button in the OMI app
2. You'll be redirected to Twitter
3. Authorize the app
4. You'll see a success message

### Step 5: Start Using!

Simply say to your OMI device:

> "Tweet Now, your amazing tweet content here!"

The app will automatically:
- Detect when you start a tweet with "Tweet Now"
- Capture your message
- Determine when your tweet is complete
- Post it to Twitter
- Confirm with a notification

## 💡 Tips

### Trigger Phrases
Start your tweet with any of these:
- "Tweet Now"
- "Post Tweet"
- "Send Tweet"
- "Tweet This"

### Ending Tweets
The AI automatically knows when you're done, but you can also say:
- "End Tweet"
- "That's It"
- "Done Tweeting"

### Examples

✅ **Good:**
```
"Tweet Now, Just had an incredible insight about AI and human creativity working together!"
```

✅ **Good with explicit end:**
```
"Tweet Now, The future of technology is voice-first. End tweet."
```

❌ **Avoid:**
```
"Tweet Now" (then pause for too long)
```

## ❓ Troubleshooting

### Issue: Authentication fails
**Solution:** 
- Check that your Twitter app has "Read and Write" permissions
- Verify the callback URL matches exactly
- Try again in a few minutes (Twitter API rate limit)

### Issue: Tweets aren't posting
**Solution:**
- Make sure you completed authentication
- Check you said "Tweet Now" to trigger
- Ensure your tweet has substantial content (20+ characters)

### Issue: Wrong content getting tweeted
**Solution:**
- Speak clearly and wait a moment after saying "Tweet Now"
- Use explicit end phrases like "End Tweet"
- Pause briefly before and after your tweet content

## 🆘 Need Help?

- Check the [full README](README.md) for detailed documentation
- Open an issue on GitHub
- Contact support via OMI app

## 🎉 That's It!

You're all set up. Start tweeting with your voice!

**Pro Tip:** The more you use it, the better the AI gets at understanding your speech patterns and tweet boundaries.

