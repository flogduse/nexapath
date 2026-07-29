# NexaPath - AI Career Copilot for Tier-2/3 India

> Team PromptX | IBM SkillsBuild | BharatCares
> Aligned with SDG 4 (Quality Education), SDG 8 (Decent Work), SDG 10 (Reduced Inequalities)

## Quick Start (Local)

### Option 1: Double-click `start.bat`
Just double-click `start.bat` — it installs everything and opens the app.

### Option 2: Manual Setup

1. **Install Python** (if not already installed)
2. `pip install -r requirements.txt`
3. `python backend\app.py`
4. Open `frontend/index.html` in your browser

## Deploy to Vercel

Deploy the entire app (backend + frontend) to Vercel for free:

1. **Install Vercel CLI**: `npm i -g vercel`
2. **Login**: `vercel login`
3. **Deploy from project root**:
   ```
   cd NexaPath
   vercel --prod
   ```
4. Your app is live at `https://nexapath.vercel.app`

**How it works on Vercel:**
- `api/index.py` wraps the Flask app as a serverless function
- `public/index.html` is served as a static site
- `vercel.json` routes `/api/*` to the Python backend and `/*` to static files
- The frontend auto-detects if it's running locally vs on Vercel

## Features

- **AI Career Agent** — Conversational AI that understands natural language, detects intent, and autonomously chains tools to guide you
- **Job Matching** — TF-IDF + Cosine Similarity algorithm matches your skills to 60+ job roles
- **Skill Gap Analysis** — Identifies missing skills and recommends free/paid courses
- **City Coverage** — 30+ Tier-2/3 Indian cities with local sector insights
- **Salary Insights** — Get salary ranges by role and category

## Dataset (v2.0 Expanded)

| Metric | Count |
|--------|-------|
| Skills | 244 |
| Job Roles | 61 |
| Cities | 34 |
| Courses | 55 |
| Interest Categories | 20 |

## Project Structure

```
NexaPath/
├── api/
│   └── index.py             # Vercel serverless entry point
├── backend/
│   ├── app.py               # Flask API server
│   ├── data/
│   │   └── jobs_dataset.json # Expanded dataset
│   └── models/
│       ├── job_matcher.py    # TF-IDF + Cosine Similarity matching
│       ├── career_agent.py   # Autonomous AI conversational agent
│       └── nexapath_model.pkl
├── frontend/
│   └── index.html           # React UI (CDN)
├── public/
│   └── index.html           # Vercel static entry
├── requirements.txt
├── vercel.json              # Vercel deployment config
├── .vercelignore
├── start.bat
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Main AI agent (conversational) |
| `/api/chat/reset` | POST | Reset conversation |
| `/api/chat/history` | GET | Get conversation log |
| `/api/match` | POST | Direct job matching |
| `/api/skill-gap` | POST | Analyze skill gaps |
| `/api/skills` | GET | List all skills |
| `/api/cities` | GET | List cities |
| `/api/jobs` | GET | Browse all job roles |
| `/api/sdgs` | GET | SDG alignment info |

## How the AI Agent Works

1. **User types a message** — e.g., "I know Python and SQL, I'm in Indore"
2. **Intent Detection** — Regex-based NLP detects intent (job search, skill gap, salary, etc.)
3. **Entity Extraction** — Extracts skills, city, job title, and interests from text
4. **Decision Engine** — Agent autonomously decides which tools to invoke
5. **Tool Chaining** — Can chain match_jobs → skill_gap → courses in a single session
6. **Formatted Response** — Returns conversational output with matching scores and recommendations

## Algorithm: TF-IDF + Cosine Similarity

**TF-IDF** (Term Frequency - Inverse Document Frequency) converts skill text into vectors, weighting rare skills higher.
**Cosine Similarity** measures the angle between user and job vectors for similarity scoring.

Final score = (Skill Match × 0.6) + (Interest Match × 0.2) + (Location Fit × 0.2)
