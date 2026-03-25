# SwasthyaSetu AI — Alzheimer's Screening App

An AI-powered web application for early Alzheimer's risk detection using cognitive assessments, voice analysis, and multi-language support.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS, Framer Motion |
| Backend | Django 4.2, Django REST Framework |
| Auth | JWT (djangorestframework-simplejwt) |
| Database | SQLite (dev) |
| Language Support | English, Hindi, Tamil, Urdu, Gujarati |

---

## Project Structure

```
├── backend/
│   ├── apps/
│   │   ├── users/          # Auth — register, login, JWT
│   │   └── screening/      # Assessments, predictions, history
│   ├── config/             # Django settings, URLs
│   ├── manage.py
│   └── requirements.txt
│
├── src/
│   ├── pages/              # Assessment, History, Result, Home, etc.
│   ├── components/         # Navbar, LoginModal, ProtectedRoute, etc.
│   ├── context/            # AuthContext, AppContext, LoginModalContext
│   ├── services/           # api.js (axios), cognitoAuth.js (fetch)
│   ├── utils/              # analyzeSymptoms.js, tokenUtils.js
│   └── i18n/               # translations.js
│
├── .env                    # VITE_API_BASE_URL=/api
├── vite.config.js          # Proxy /api → localhost:8000
├── tailwind.config.js
└── package.json
```

---

## Getting Started

### Requirements
- Python 3.10+
- Node.js 18+

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Runs at `http://localhost:8000`

### 2. Frontend

```bash
# from project root
npm install
npm run dev
```

Runs at `http://localhost:5173`

---

## Environment Variables

`.env` (project root):
```
VITE_API_BASE_URL=/api
NODE_ENV=development
```

---

## API Endpoints

### Auth — `/api/auth/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | Create account |
| POST | `/login/` | Login, returns JWT |
| GET | `/me/` | Current user info |
| POST | `/logout/` | Logout |

### Screening — `/api/screening/`
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/prediction/` | Run Alzheimer's risk prediction |
| POST | `/save/` | Save assessment result |
| GET | `/history/` | Get user's assessment history |
| POST | `/memory/` | Memory assessment |
| POST | `/voice/` | Voice transcription |
| POST | `/phc-finder/` | Find nearby health centers |
| GET | `/result/<id>/` | Get specific result |

---

## Features

- Register / Login with JWT authentication
- 32-feature cognitive assessment form
- Risk prediction (Low / Medium / High) with probability score
- Assessment history saved per user
- Voice input support via Web Speech API
- Multi-language UI (English, Hindi, Tamil, Urdu, Gujarati)
- PHC Finder for nearby health centers
- Responsive, mobile-friendly design

---

## Authentication Flow

1. User registers with email + password
2. Backend hashes password and stores user
3. Login returns a JWT access token
4. Frontend stores token in `localStorage`
5. All protected API calls send `Authorization: Bearer <token>`

---

## Troubleshooting

**Backend won't start**
```bash
pip install -r requirements.txt
python manage.py migrate
```

**Frontend shows "Failed to fetch"**
- Make sure backend is running on port `8000`
- Check `.env` has `VITE_API_BASE_URL=/api`
- Restart frontend after `.env` changes: `npm run dev`

**CORS errors**
- Vite proxies `/api` to `localhost:8000` — no direct cross-origin calls needed
- If calling backend directly, update `CORS_ALLOWED_ORIGINS` in `backend/config/settings.py`

---

## License

Part of the Cloud Knight hackathon project — March 2026.
