# 🏥 MediBot — AI Medical Assistant

> A multimodal medical AI chatbot that supports text, image analysis, and PDF report summarization — built for patients seeking quick, AI-powered medical insights.

**🔴 Live Demo:** [https://medibot-ui.netlify.app](https://medibot-ui.netlify.app)  
**🔗 Backend API:** [https://medibot-fizw.onrender.com](https://medibot-fizw.onrender.com)  
**📄 API Docs:** [https://medibot-fizw.onrender.com/docs](https://medibot-fizw.onrender.com/docs)

---

## 🚀 Features

- **Text Chat** — Ask medical questions and get AI-powered responses using LLaMA 3.3 70B via Groq
- **Image Analysis** — Upload medical images (X-rays, skin conditions, reports) and get AI-driven visual analysis
- **PDF Summarization** — Upload medical reports/documents and get structured summaries with key findings highlighted
- **Session Memory** — Full conversation history stored per session using SQLite
- **Fast Inference** — Powered by Groq's ultra-low latency inference API

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq + LLaMA 3.3 70B |
| Vision | Groq LLaVA |
| PDF | PyMuPDF |
| Backend | FastAPI + SQLite |
| Frontend | HTML + CSS + JavaScript |
| Deployment | Docker + Render (backend), Netlify (frontend) |

---

## 🏗️ Project Structure

```
MediBot/
├── backend/
│   └── app/
│       ├── db/          # SQLAlchemy models and database setup
│       ├── routes/      # FastAPI route handlers (chat, upload, voice)
│       ├── schemas/     # Pydantic request/response models
│       ├── services/    # Business logic (LLM, vision, PDF, speech)
│       └── main.py      # FastAPI app entry point
├── core/
│   ├── llm/             # Groq client and prompt builder
│   ├── speech/          # STT/TTS modules
│   └── vision/          # Image encoder and vision analyzer
├── frontend/
│   └── index.html       # Single-file frontend UI
├── utils/               # Logger, validators, file handler
├── config.py            # Pydantic settings
├── Dockerfile
└── requirements.txt
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Docker (optional)
- Groq API Key → [console.groq.com](https://console.groq.com)

### 1. Clone the repo
```bash
git clone https://github.com/AyushWorks-24/MediBot.git
cd MediBot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Create a `.env` file in the root:
```env
GROQ_API_KEY=your_groq_api_key
TTS_PROVIDER=gtts
APP_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite+aiosqlite:///./medibot.db
MAX_UPLOAD_SIZE_MB=10
UPLOAD_DIR=uploads/
```

### 5. Run the backend
```bash
uvicorn backend.app.main:app --reload
```

### 6. Open the frontend
Open `frontend/index.html` in your browser or serve it:
```bash
python -m http.server 3000 --directory frontend
```

---

## 🐳 Docker

```bash
docker build -t medibot .
docker run -p 8000:8000 --env-file .env medibot
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat/` | Send a text message |
| GET | `/chat/history/{session_id}` | Get session history |
| POST | `/chat/new-session` | Create new session |
| POST | `/upload/image` | Upload and analyze image |
| POST | `/upload/pdf` | Upload and summarize PDF |

---

## ⚠️ Disclaimer

MediBot is an AI assistant for informational purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## 👨‍💻 Author

**Ayush Kumar**  
B.Tech AI & ML — Oriental College of Technology, Bhopal  
📧 ayushkumars1609@gmail.com  
🐙 [github.com/AyushWorks-24](https://github.com/AyushWorks-24)