# 🚀 Deployment Guide

This guide covers deploying the OMI Twitter Integration to various cloud platforms.

## 🎯 Prerequisites

Before deploying:
- ✅ Twitter Developer Account with API credentials
- ✅ OpenAI API key
- ✅ Git repository (GitHub, GitLab, etc.)

## 🔥 Quick Deploy Options

### Railway.app (Recommended - Easiest)

1. **Create Account**
   - Visit [Railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy**
   ```bash
   # Install Railway CLI (optional)
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   railway up
   ```
   
   Or use the web interface:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   - Go to your project
   - Click "Variables"
   - Add all variables from `.env.example`
   - Important: Set `OAUTH_REDIRECT_URL` to your Railway URL

4. **Get Your URL**
   - Railway auto-generates a URL like: `your-app.up.railway.app`
   - Update `OAUTH_REDIRECT_URL` to: `https://your-app.up.railway.app/auth/callback`
   - Update this in both Railway variables AND Twitter Developer Portal

5. **Update Twitter App**
   - Go to Twitter Developer Portal
   - Update Callback URLs with your Railway URL
   - Save changes

### Render.com

1. **Create Account**
   - Visit [Render.com](https://render.com)
   - Sign in with GitHub

2. **Deploy**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: omi-twitter-integration
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - Add all variables from `.env.example`
   - Set `OAUTH_REDIRECT_URL` to your Render URL

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)

### Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from heroku.com
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set TWITTER_API_KEY=xxx
   heroku config:set TWITTER_API_SECRET=xxx
   heroku config:set TWITTER_CLIENT_ID=xxx
   heroku config:set TWITTER_CLIENT_SECRET=xxx
   heroku config:set OPENAI_API_KEY=xxx
   heroku config:set OAUTH_REDIRECT_URL=https://your-app-name.herokuapp.com/auth/callback
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Update Twitter App**
   - Add Heroku URL to Twitter Callback URLs

### DigitalOcean App Platform

1. **Create Account**
   - Visit [DigitalOcean](https://www.digitalocean.com)

2. **Deploy**
   - Go to Apps → Create App
   - Connect GitHub repository
   - Configure:
     - **Type**: Web Service
     - **Run Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - Add all required variables
   - Set `OAUTH_REDIRECT_URL`

4. **Deploy**
   - Click "Create Resources"

### Google Cloud Run

1. **Install gcloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Initialize
   gcloud init
   ```

2. **Create Dockerfile** (if not exists)
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

3. **Deploy**
   ```bash
   gcloud run deploy omi-twitter \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Set Environment Variables**
   - Go to Cloud Run console
   - Select your service
   - Edit → Variables & Secrets
   - Add all required variables

### AWS (Elastic Beanstalk)

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize**
   ```bash
   eb init -p python-3.11 omi-twitter
   ```

3. **Create Environment**
   ```bash
   eb create omi-twitter-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv TWITTER_API_KEY=xxx TWITTER_API_SECRET=xxx ...
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

## 🔧 Post-Deployment Checklist

After deploying to any platform:

- [ ] ✅ Get your deployment URL
- [ ] ✅ Update `OAUTH_REDIRECT_URL` in your environment variables
- [ ] ✅ Update Twitter Developer Portal with new callback URL
- [ ] ✅ Test the `/health` endpoint: `https://your-url/health`
- [ ] ✅ Test authentication flow: `https://your-url/auth?uid=test123`
- [ ] ✅ Configure OMI app with your webhook URLs:
  - Webhook: `https://your-url/webhook`
  - Auth: `https://your-url/auth`
  - Setup Check: `https://your-url/setup-completed`

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` to version control
   - Use platform secret management
   - Rotate keys regularly

2. **HTTPS**
   - Always use HTTPS in production
   - Most platforms provide free SSL

3. **Rate Limiting**
   - Consider adding rate limiting
   - Monitor API usage

4. **Database**
   - For production, use PostgreSQL instead of SQLite
   - Update `DATABASE_URL` accordingly

5. **Monitoring**
   - Set up error tracking (Sentry)
   - Monitor logs
   - Set up uptime monitoring

## 🗄️ Using PostgreSQL (Recommended for Production)

### Railway/Render/Heroku

1. **Add PostgreSQL**
   - Railway: Add PostgreSQL from "New" menu
   - Render: Create new PostgreSQL database
   - Heroku: `heroku addons:create heroku-postgresql:mini`

2. **Update Environment**
   ```bash
   # Railway/Render auto-set DATABASE_URL
   # For Heroku, it's automatic
   
   # If manual:
   DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
   ```

3. **Update requirements.txt**
   ```txt
   # Add to requirements.txt
   asyncpg==0.29.0
   ```

4. **Database Migrations** (Optional)
   ```bash
   # Install Alembic
   pip install alembic
   
   # Initialize
   alembic init alembic
   
   # Create migration
   alembic revision --autogenerate -m "initial"
   
   # Apply migration
   alembic upgrade head
   ```

## 📊 Monitoring & Logs

### View Logs

**Railway**
```bash
railway logs
```

**Render**
- View in dashboard under "Logs"

**Heroku**
```bash
heroku logs --tail
```

### Error Tracking

Add Sentry (optional):
```bash
pip install sentry-sdk
```

```python
# In main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

## 🧪 Testing Deployment

1. **Health Check**
   ```bash
   curl https://your-url/health
   ```

2. **Authentication Flow**
   ```bash
   # Visit in browser
   https://your-url/auth?uid=test123
   ```

3. **Webhook Test**
   ```bash
   curl -X POST "https://your-url/webhook?session_id=test&uid=test123" \
     -H "Content-Type: application/json" \
     -d '[{"text": "test", "speaker": "SPEAKER_00"}]'
   ```

## 💰 Cost Estimates

| Platform | Free Tier | Paid |
|----------|-----------|------|
| Railway | $5 credit/month | ~$5-20/month |
| Render | 750 hours/month | $7+/month |
| Heroku | Eco dyno | $5+/month |
| DigitalOcean | $200 credit | $5+/month |
| Google Cloud | $300 credit | Pay as you go |

## 🆘 Troubleshooting

### Issue: App crashes on startup
- Check logs for errors
- Verify all environment variables are set
- Ensure port binding is correct (`$PORT` variable)

### Issue: OAuth redirect not working
- Verify `OAUTH_REDIRECT_URL` matches Twitter settings exactly
- Use HTTPS in production
- Check callback URL includes `/auth/callback`

### Issue: Database errors
- For SQLite, ensure writable filesystem
- Consider switching to PostgreSQL for production
- Check `DATABASE_URL` format

### Issue: High memory usage
- Monitor usage in platform dashboard
- Consider scaling to higher tier
- Optimize database queries

## 📈 Scaling

When you need more resources:

1. **Vertical Scaling**
   - Upgrade to higher tier on your platform
   - Increase RAM and CPU

2. **Horizontal Scaling**
   - Add more instances (most platforms auto-scale)
   - Use load balancer (usually built-in)

3. **Database Scaling**
   - Use connection pooling
   - Upgrade to managed PostgreSQL
   - Add read replicas

4. **Caching**
   - Add Redis for session management
   - Cache user tokens

## 🎓 Next Steps

After successful deployment:
- [ ] Submit your app to OMI marketplace
- [ ] Add monitoring and alerts
- [ ] Set up automated backups
- [ ] Create staging environment
- [ ] Add custom domain (optional)

---

**Need help?** Check the main [README.md](README.md) or open an issue on GitHub.

