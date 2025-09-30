voice-cbt/
├── README.md
├── docker-compose.yml
├── .env.template
├── package.json
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── audio.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── services/
│   │   │   ├── emotion.py
│   │   │   ├── reply.py
│   │   │   └── tts.py
│   │   └── models/
│   │       └── schemas.py
├── frontend/
│   ├── Dockerfile
│   ├── next.config.js
│   ├── package.json
│   ├── pages/
│   │   ├── index.tsx
│   │   └── history.tsx
│   ├── components/
│   │   ├── Waveform.tsx
│   │   ├── EmotionBar.tsx
│   │   └── Navbar.tsx
│   ├── lib/
│   │   └── api.ts
│   └── styles/
│       └── globals.css
└── nginx/
    └── default.conf   # optional reverse proxyi