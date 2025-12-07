# Deployment Guide for Render

## Prerequisites
- GitHub account
- Render account (https://render.com)
- Valid Gemini API key
- Qdrant Cloud account with credentials

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create New Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`

### 3. Configure Environment Variables
Add these in Render Dashboard → Environment:

```
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 4. Deploy
- Click "Create Web Service"
- Wait for build to complete (~10-15 minutes for first deploy)

## Important Notes

### Memory Warnings
- `sentence-transformers` model is ~400MB
- Render free tier has 512MB RAM
- If deployment fails with OOM error, upgrade to Starter plan ($7/mo)

### Cold Starts
- Free tier spins down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to warm up

### `/build-index` Endpoint
- **Takes 30-60+ seconds** to complete (fetches 36 URLs)
- May timeout on Render free tier (30s limit)
- Consider running this locally or using background workers

## Production Recommendations

### 1. Use Background Tasks for Indexing
```python
from fastapi import BackgroundTasks

@app.post("/build-index")
async def build_index(background_tasks: BackgroundTasks):
    background_tasks.add_task(index_all_pages)
    return {"status": "indexing_started"}
```

### 2. Pre-build Index
Run `build-index` locally before deployment:
```bash
curl -X POST http://localhost:8000/build-index
```

### 3. Add Rate Limiting
Install `slowapi` for rate limiting:
```bash
pip install slowapi
```

### 4. Monitor Usage
- Check logs: Render Dashboard → Logs
- Monitor Gemini API usage: https://ai.dev/usage
- Monitor Qdrant usage: Qdrant Cloud Dashboard

## Troubleshooting

### Build Fails
- Check `requirements.txt` versions are compatible
- Increase disk space if needed

### Health Check Fails
- Model loading takes too long (13s+)
- Increase health check timeout in Render settings

### Out of Memory
- Upgrade to paid plan
- Use smaller embedding model

### API Key Errors
- Ensure environment variables are set correctly
- Check Gemini API quota at https://ai.dev/usage

## Testing Deployment

Once deployed, test endpoints:

```bash
# Health check
curl https://your-app.onrender.com/health

# Chat endpoint
curl -X POST https://your-app.onrender.com/chat \
  -F "query=What is ROS2?"
```
