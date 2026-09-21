# English Placement Test

A full-stack English proficiency placement system.

Users register, take a multiple-choice exam, and get a CEFR level (A1–C2) based on their score. Built with a Python backend and a clean, minimal frontend.

---

##  Features

* User registration and JWT login
* Random exam questions (up to 20)
* Automatic scoring and CEFR mapping
* Progress history for each user
* Admin CEFR distribution endpoint
* Single server for API + UI

---

##  Tech Stack

| Layer        | Tools                               |
| ------------ | ----------------------------------- |
| **Backend**  | FastAPI, SQLAlchemy, JWT, bcrypt    |
| **Database** | SQLite (local)                      |
| **Frontend** | HTML, CSS, vanilla JavaScript       |
| **Auth**     | OAuth2 password flow + Bearer token |

---

##  Project Structure

```text
english_placement/
├── backend/
│   ├── app/
│   │   ├── api/          # routes + auth dependencies
│   │   ├── core/         # config, JWT, password hashing
│   │   ├── db/           # database session
│   │   ├── models/       # User, Question, Exam, Result
│   │   ├── schemas/      # request/response models
│   │   ├── services/     # scoring, sampling, pagination
│   │   └── main.py       # FastAPI app + static UI
│   ├── scripts/          # seed questions, make admin
│   ├── tests/
│   ├── create_tables.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/styles.css
│   └── js/
│       ├── api.js        # API calls
│       └── app.js        # UI logic
└── README.md
```

---

##  Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\activate
$env:PYTHONPATH = "."
pip install -r requirements.txt
python create_tables.py
python scripts\seed_sample_questions.py
```

#### Linux / macOS

```bash
source .venv/bin/activate
export PYTHONPATH=.
pip install -r requirements.txt
python create_tables.py
python scripts/seed_sample_questions.py
```

### 2. Run the App

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open in your browser:

| URL                            | What it is       |
| ------------------------------ | ---------------- |
| `http://localhost:8000/`       | Web UI           |
| `http://localhost:8000/docs`   | Swagger API docs |
| `http://localhost:8000/health` | Health check     |

---

##  How to Use the UI

1. **Register** with email + password (min 8 characters)
2. **Login**
3. Click **Start exam**
4. Answer the questions (Previous / Next)
5. **Submit** to see your score and CEFR level
6. Open **Progress** to view past results

---

## 🔌 Main API Endpoints

| Method | Path                              | Description                        |
| ------ | --------------------------------- | ---------------------------------- |
| `POST` | `/api/v1/auth/register`           | Create account                     |
| `POST` | `/api/v1/auth/login`              | Get JWT (form: `username` = email) |
| `POST` | `/api/v1/exams/start`             | Start exam, get questions          |
| `POST` | `/api/v1/results/submit`          | Submit answers, get score + CEFR   |
| `GET`  | `/api/v1/progress/`               | User progress over time            |
| `GET`  | `/api/v1/history/`                | Paginated exam history             |
| `GET`  | `/api/v1/admin/cefr-distribution` | Admin-only stats                   |

Login expects `application/x-www-form-urlencoded` with fields `username` and `password` (OAuth2 style).

---

##  Optional Scripts

```bash

python scripts/make_admin.py you@example.com


python scripts/import_questions.py
```

---

##  Tests

```bash
cd backend


pytest tests/ -v
```

---

##  CEFR Mapping (Simplified)

Score percentage is mapped to levels A1 → C2 by the scoring service.

Exact thresholds live in:

```text
backend/app/services/scoring.py
```

---

##  Notes

* Local database file: `backend/english.db` (ignored by git)
* JWT is stored in the browser `localStorage`
* CORS is open for local development; tighten it for production
* `.venv`, `__pycache__`, and `*.db` are in `.gitignore`

---

##  Possible Next Improvements

* More questions and better difficulty balance
* Docker / production config
* Stronger password rules and rate limiting
* Deploy to Render, Railway, or similar

---

## 📄 License

See `LICENSE` in the repository root.
