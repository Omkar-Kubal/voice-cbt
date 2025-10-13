# Voice CBT Deployment Guide

## Frontend Deployment on Vercel

### Step 1: Prepare Frontend for Vercel

1. **Create `frontend/vercel.json`:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

2. **Create `frontend/.env.example`:**
```env
VITE_API_URL=https://your-backend-url.railway.app
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef
```

### Step 2: Deploy Frontend to Vercel

1. **Go to [vercel.com](https://vercel.com) and sign in**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure the project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

5. **Set Environment Variables in Vercel:**
   - `VITE_API_URL` = Your backend URL (from Railway/Render)
   - `VITE_FIREBASE_API_KEY` = Your Firebase API key
   - `VITE_FIREBASE_AUTH_DOMAIN` = Your Firebase auth domain
   - `VITE_FIREBASE_PROJECT_ID` = Your Firebase project ID
   - `VITE_FIREBASE_STORAGE_BUCKET` = Your Firebase storage bucket
   - `VITE_FIREBASE_MESSAGING_SENDER_ID` = Your Firebase messaging sender ID
   - `VITE_FIREBASE_APP_ID` = Your Firebase app ID

6. **Deploy!**

## Backend Deployment Options

### Option A: Railway (Recommended for Python/FastAPI)

1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Select the `backend` folder as root directory**
4. **Railway will automatically detect Python and install dependencies**
5. **Set environment variables:**
   - `OPENAI_API_KEY` = Your OpenAI API key
   - `GEMINI_API_KEY` = Your Gemini API key
   - `JWT_SECRET` = Your JWT secret
   - `SECRET_KEY` = Your secret key
   - `DATABASE_URL` = SQLite (Railway will handle this)

### Option B: Render

1. **Go to [render.com](https://render.com)**
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Option C: Vercel (Serverless Functions)

For Vercel backend deployment, you'll need to restructure your FastAPI app:

1. **Create `api/` folder in root**
2. **Move FastAPI routes to individual serverless functions**
3. **Use Vercel's serverless functions**

## Environment Variables Setup

### Frontend (Vercel)
```env
VITE_API_URL=https://your-backend-url.railway.app
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef
```

### Backend (Railway/Render)
```env
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET=your_jwt_secret
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./voice_cbt.db
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

## Post-Deployment Steps

1. **Update CORS settings** in backend to allow your Vercel domain
2. **Test the connection** between frontend and backend
3. **Set up Firebase authentication** if using auth features
4. **Configure domain** (optional) for custom domain

## Troubleshooting

- **CORS Issues:** Make sure backend CORS_ORIGINS includes your Vercel domain
- **Build Failures:** Check that all dependencies are in package.json/requirements.txt
- **Environment Variables:** Ensure all required env vars are set in both services
- **Database:** Railway/Render will handle SQLite automatically

## Recommended Architecture

```
Frontend (Vercel) → Backend (Railway) → Database (SQLite)
     ↓                    ↓
Firebase Auth      OpenAI/Gemini APIs
```

This setup provides:
- ✅ Fast frontend delivery via Vercel CDN
- ✅ Reliable backend hosting on Railway
- ✅ Automatic scaling
- ✅ Easy environment management
- ✅ Cost-effective for small to medium projects
