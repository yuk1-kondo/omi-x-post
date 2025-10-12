# 🚀 Railway Deployment Guide

## Quick Deploy (Web Interface - Easiest!)

### Option 1: Deploy via Railway Dashboard (No CLI needed!)

1. **Go to Railway**
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository

3. **Configure Environment Variables**
   
   Click on your project → Variables → Add these (copy from your .env file):
   
   ```bash
   TWITTER_API_KEY=your_twitter_api_key_here
   TWITTER_API_SECRET=your_twitter_api_secret_here
   TWITTER_CLIENT_ID=your_twitter_client_id_here
   TWITTER_CLIENT_SECRET=your_twitter_client_secret_here
   OPENAI_API_KEY=your_openai_api_key_here
   APP_HOST=0.0.0.0
   APP_PORT=8000
   DATABASE_URL=sqlite+aiosqlite:///./twitter_omi.db
   ```
   
   **IMPORTANT:** Leave `OAUTH_REDIRECT_URL` blank for now

4. **Deploy!**
   - Railway will automatically build and deploy
   - Wait 2-3 minutes
   - You'll get a URL like: `your-app.up.railway.app`

5. **Get Your Railway URL**
   - Click "Settings" → "Networking"
   - Click "Generate Domain"
   - Copy your Railway URL (e.g., `twitter-production.up.railway.app`)

6. **Update Environment Variable**
   - Go back to Variables
   - Add: `OAUTH_REDIRECT_URL=https://YOUR-RAILWAY-URL/auth/callback`
   - Example: `OAUTH_REDIRECT_URL=https://twitter-production.up.railway.app/auth/callback`

7. **Update Twitter Developer Portal**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Click your app → User authentication settings → Edit
   - Update Callback URLs: `https://YOUR-RAILWAY-URL/auth/callback`
   - Save

8. **Done!** 🎉
   - Your app is live at: `https://YOUR-RAILWAY-URL`
   - Test page: `https://YOUR-RAILWAY-URL/test`

---

## Option 2: Deploy via CLI

### Install Railway CLI

```bash
# macOS
brew install railway

# Or use npm
npm i -g @railway/cli
```

### Deploy Steps

```bash
# 1. Login to Railway
railway login

# 2. Initialize project
railway init

# 3. Link to a new project
railway link

# 4. Add environment variables
railway variables set TWITTER_API_KEY=xxx
railway variables set TWITTER_API_SECRET=xxx
railway variables set TWITTER_CLIENT_ID=xxx
railway variables set TWITTER_CLIENT_SECRET=xxx
railway variables set OPENAI_API_KEY=xxx
railway variables set APP_HOST=0.0.0.0
railway variables set APP_PORT=8000

# 5. Deploy!
railway up

# 6. Get your URL
railway domain

# 7. Add OAuth redirect URL
railway variables set OAUTH_REDIRECT_URL=https://YOUR-RAILWAY-URL/auth/callback
```

---

## 📱 Configure OMI App with New URLs

Once deployed, update your OMI app settings:

| Field | New Value |
|-------|-----------|
| **Webhook URL** | `https://YOUR-RAILWAY-URL/webhook` |
| **App Home URL** | `https://YOUR-RAILWAY-URL/` |
| **Auth URL** | `https://YOUR-RAILWAY-URL/auth` |
| **Setup Completed URL** | `https://YOUR-RAILWAY-URL/setup-completed` |

---

## ✅ Post-Deployment Checklist

- [ ] Railway app deployed and running
- [ ] Got your permanent Railway URL
- [ ] Updated `OAUTH_REDIRECT_URL` in Railway variables
- [ ] Updated Twitter Developer Portal callback URL
- [ ] Updated OMI app webhook URLs
- [ ] Tested authentication at: `https://YOUR-RAILWAY-URL/test`
- [ ] Tested tweeting with OMI device

---

## 💰 Railway Pricing

- **Free tier**: $5 credit/month
- **Hobby**: $5/month for more resources
- **Your app**: Should use ~$3-5/month on hobby plan

---

## 🐛 Troubleshooting

### App won't start
- Check Deployment Logs in Railway dashboard
- Verify all environment variables are set
- Check that `main_simple.py` is being run

### OAuth errors
- Make sure `OAUTH_REDIRECT_URL` uses HTTPS
- Verify it matches Twitter callback URL exactly
- Must include `/auth/callback` at the end

### Port binding issues
- Railway auto-sets `PORT` env var
- Our app uses `APP_PORT` - should work fine

---

## 🎯 Benefits of Railway vs Ngrok

| Feature | Ngrok | Railway |
|---------|-------|---------|
| URL Changes | Every restart | Never |
| HTTPS | ✅ | ✅ |
| Uptime | While running locally | 24/7 |
| Cost | Free (limited) | $5/month |
| Re-auth needed | After each URL change | Once |

---

**Ready to deploy?** Follow Option 1 (Web Interface) - it's the easiest! 🚀

