# Vercel Deployment Guide for Voice CBT

## 🚀 Deploy Frontend to Vercel

### Step 1: Prepare for Deployment

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

### Step 2: Deploy Frontend

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Deploy to Vercel**:
   ```bash
   vercel
   ```

3. **Follow the prompts**:
   - Link to existing project? **No**
   - Project name: `voice-cbt-frontend`
   - Directory: `./frontend`
   - Override settings? **No**

### Step 3: Configure Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add these variables:

```
VITE_API_URL=https://your-backend-url.railway.app
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
```

### Step 4: Deploy Backend (Alternative Options)

#### Option A: Railway (Recommended)
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy the backend service
4. Get the Railway URL for your backend

#### Option B: Render
1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 5: Update API URLs

After getting your backend URL, update the `vercel.json` file:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-actual-backend-url.railway.app/api/$1"
    }
  ],
  "env": {
    "VITE_API_URL": "https://your-actual-backend-url.railway.app"
  }
}
```

### Step 6: Redeploy

After updating the configuration:

```bash
cd frontend
vercel --prod
```

## 🔧 Configuration Details

### Frontend Configuration
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Node Version**: 18.x

### Backend Configuration
- **Platform**: Railway/Render
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Python Version**: 3.11+

## 🌐 Access Your App

After deployment:
- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://your-backend.railway.app`

## 📝 Notes

1. **CORS**: Make sure your backend allows requests from your Vercel domain
2. **Environment Variables**: Update all API URLs in your frontend
3. **Database**: Ensure your database is accessible from the deployed backend
4. **SSL**: Both Vercel and Railway provide SSL certificates automatically

## 🚨 Troubleshooting

### Common Issues:
1. **Build Failures**: Check your `package.json` scripts
2. **API Errors**: Verify your backend URL and CORS settings
3. **Environment Variables**: Make sure all required variables are set
4. **Database Connection**: Ensure your database is accessible from the cloud

### Debug Commands:
```bash
# Check Vercel deployment status
vercel ls

# View deployment logs
vercel logs

# Check environment variables
vercel env ls
```
