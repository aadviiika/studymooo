# 🐄 StudyMoo

> Share knowledge. Learn together.

---

## ⚡ Run Locally

```bash
# 1. Run setup (creates venv, installs deps, migrates, seeds courses)
python3 setup.py

# 2. Activate venv and start server
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows

cd studymoo_project
python manage.py runserver
```

Open → http://127.0.0.1:8000

---

## 🚀 Deploy on Render (recommended)

1. Push this folder to a GitHub repo
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Add environment variable `SECRET_KEY` with any long random string

That's it. Render handles everything else.

---

## 🚀 Deploy on Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. In **Settings** set:
   - **Build Command:** `pip install -r studymoo_project/requirements.txt && python studymoo_project/manage.py collectstatic --noinput`
   - **Start Command:** `python studymoo_project/manage.py migrate && gunicorn --bind 0.0.0.0:$PORT studymoo_project.wsgi:application`
4. Add Variables: `SECRET_KEY`, `DEBUG=False`

---

## 📁 Structure

```
studymoonew/
├── setup.py               ← one-click local setup
├── render.yaml            ← Render deployment config
├── .gitignore
└── studymoo_project/
    ├── manage.py
    ├── requirements.txt
    ├── studymoo_project/  ← Django config
    │   ├── settings.py
    │   └── urls.py
    ├── resources/         ← main app
    ├── templates/
    ├── static/
    └── media/             ← uploaded files (auto-created)
```
