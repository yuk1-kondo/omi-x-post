# 🌐 Ngrok Setup Guide

## Step-by-Step Instructions

### Terminal 1: Start the App

```bash
cd /Users/aaravgarg/omi-ai/Code/apps/twitter

# Activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (if not already)
pip install -r requirements.txt

# Start the app
python main.py
```

Keep this terminal running! You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### Terminal 2: Start Ngrok

Open a **NEW terminal** and run:

```bash
ngrok http 8000
```

You'll see something like:
```
Forwarding   https://1234-56-78-90-12.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://1234-56-78-90-12.ngrok.io`)

---

## 🔧 Update Configuration

### 1. Update .env file

Replace the ngrok URL in your `.env`:

```bash
OAUTH_REDIRECT_URL=https://YOUR-NGROK-URL.ngrok.io/auth/callback
```

Then **restart the app** in Terminal 1 (Ctrl+C and run `python main.py` again)

### 2. Update Twitter Developer Portal

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Select your app
3. Go to **App Settings** → **User authentication settings**
4. Update **Callback URLs**:
   ```
   https://YOUR-NGROK-URL.ngrok.io/auth/callback
   ```
5. Save changes

---

## 📱 Configure OMI App

In the OMI mobile app:

1. Go to **Settings** → **Developer Mode** (enable it)
2. Go to **Developer Settings**
3. Create new Integration App or update existing:
   - **Webhook URL**: `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - **Auth URL**: `https://YOUR-NGROK-URL.ngrok.io/auth`
   - **Setup Completed URL**: `https://YOUR-NGROK-URL.ngrok.io/setup-completed`

---

## ✅ Test It!

### 1. Test Health Check

Visit in browser:
```
https://YOUR-NGROK-URL.ngrok.io/health
```

Should return: `{"status": "healthy"}`

### 2. Authenticate Twitter

In OMI app, click **Authenticate** button for your integration.

### 3. Test Tweet!

Say to your OMI device:
```
"Tweet Now, This is my first voice-activated tweet!"
```

Check your Twitter timeline! 🎉

---

## 🔄 Important Notes

- **Ngrok URL changes** every time you restart ngrok (unless you have a paid plan)
- When ngrok URL changes, update:
  - `.env` file
  - Twitter Developer Portal
  - OMI app settings
  - Restart the FastAPI app

- **Free tier limitations**:
  - URL changes on restart
  - 40 connections/minute
  - Session expires after 8 hours

- **Pro tip**: Get ngrok paid plan for static domain if using frequently

---

## 🐛 Troubleshooting

### "OAuth redirect not working"
- Make sure OAUTH_REDIRECT_URL in .env matches Twitter settings EXACTLY
- Include `/auth/callback` at the end
- Use HTTPS (ngrok provides this automatically)
- Restart the app after changing .env

### "Ngrok tunnel closed"
- Free plan has connection limits
- Restart ngrok if it crashes
- Update URLs if tunnel URL changed

### "App not receiving webhooks"
- Check ngrok is still running
- Verify webhook URL in OMI app is correct
- Check Terminal 1 for app logs

---

## 🚀 Alternative: Deploy for Production

For permanent URLs without ngrok hassle, deploy to:
- **Railway** (recommended): See DEPLOYMENT.md
- **Render**
- **Heroku**

These give you permanent URLs that don't change!

