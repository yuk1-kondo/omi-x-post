# ⚡ Quick Start Guide

Get your OMI Twitter Integration up and running in 5 minutes!

## 📋 Prerequisites Checklist

- [ ] Twitter Developer Account ([Sign up here](https://developer.twitter.com/en/portal/dashboard))
- [ ] OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))
- [ ] Python 3.8+ installed
- [ ] OMI device and app

## 🚀 5-Minute Setup

### Step 1: Get API Keys (2 minutes)

**Twitter:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create app → Enable OAuth 2.0 → Set callback URL
3. Copy: API Key, API Secret, Client ID, Client Secret

**OpenAI:**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create new key → Copy it

### Step 2: Install (1 minute)

```bash
# Navigate to project
cd /path/to/twitter

# Run start script (it handles everything)
./start.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
python main.py
```

### Step 3: Configure OMI App (1 minute)

1. Open OMI app
2. Settings → Developer Mode → ON
3. Developer Settings → Create App
4. Fill in:
   - **Webhook**: `http://your-url:8000/webhook`
   - **Auth**: `http://your-url:8000/auth`
   - **Setup Check**: `http://your-url:8000/setup-completed`

### Step 4: Authenticate (30 seconds)

1. Click "Authenticate" in OMI app
2. Login to Twitter
3. Authorize the app
4. Done! ✅

### Step 5: Test It! (30 seconds)

Say to your OMI:
```
"Tweet Now, This is my first voice tweet!"
```

Check your Twitter - it should be there! 🎉

## 🎯 That's It!

You're ready to tweet with your voice. Just say:
- "Tweet Now" + your message
- AI detects when you're done
- Tweet posts automatically

## 📚 Learn More

- **Full Setup**: [README.md](README.md)
- **Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🆘 Troubleshooting

### Server won't start
```bash
# Check if .env is configured
cat .env

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Authentication fails
- Verify Twitter callback URL matches exactly
- Check API keys are correct
- Try in incognito/private browser window

### Tweets not posting
- Complete authentication first
- Check you said "Tweet Now"
- Ensure tweet has 20+ characters

## 💡 Pro Tips

1. **Deploy for 24/7 access**: Use Railway or Render (see [DEPLOYMENT.md](DEPLOYMENT.md))
2. **Practice makes perfect**: Start with simple tweets
3. **Use explicit endings**: Say "End tweet" while learning
4. **Check confirmations**: Wait for OMI to confirm before next tweet

## 🎓 Next Steps

1. ✅ Basic tweeting works
2. 📖 Read [EXAMPLES.md](EXAMPLES.md) for advanced usage
3. 🚀 Deploy to cloud for always-on access
4. 🎨 Customize trigger phrases in `tweet_detector.py`
5. 📊 Add analytics or additional features

## 🤝 Need Help?

- 📝 Check [README.md](README.md) for detailed docs
- 🐛 [Open an issue](https://github.com/yourusername/twitter/issues)
- 💬 Ask in OMI community

---

**Happy Voice Tweeting!** 🐦✨

