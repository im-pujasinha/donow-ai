# 🔥 DoNow — Stop Procrastinating

> An AI-powered anti-procrastination engine built for students who can't start tasks and get distracted by social media.

**Vibe2Ship Hackathon** · Problem Statement: The Last-Minute Life Saver

---

## 🚀 Live Demo
[Deployed on Google Cloud Run] → *(add link after deployment)*

---

## 🎯 Problem

Students miss deadlines not because they don't know what to do — but because they **can't start**, and **social media pulls them away** the moment they try. Generic task apps just list tasks. DoNow actively fights procrastination.

---

## ✨ Key Features

| Feature | What it does |
|---|---|
| 🧠 **Brutal AI Prioritization** | Gemini analyzes tasks with no sugarcoating — tells you what's urgent and why |
| ▶ **One-Click Start** | Every task has a "start phrase" — the exact first physical action to take |
| ⏱ **Focus Mode + Pomodoro Timer** | 25-min countdown, phone-down reminders, subtask checklist |
| 📵 **Distraction Risk Flags** | AI flags which tasks you're most likely to procrastinate on |
| 🗓️ **Smart Schedule Generator** | Builds your day in Pomodoro blocks around your actual task list |
| 💬 **Blunt AI Coach** | Calls out your excuses, gives direct actionable advice |
| 🔥 **Streak Tracking** | Daily completion streaks to build discipline |

---

## 🛠️ Technologies Used

- **Python 3.11**
- **Streamlit** — UI framework
- **Google Gemini 2.5 Flash** — AI core (prioritization, coaching, scheduling)
- **Docker** — Containerization
- **Google Cloud Run** — Deployment

---

## 🔧 Google Technologies

- **Gemini 2.5 Flash API** — Task analysis, schedule generation, AI coaching
- **Google Cloud Run** — Serverless container deployment
- **Google AI Studio** — Model access and API management

---

## 🏃 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/donow-ai
cd donow-ai
pip install -r requirements.txt
streamlit run app.py
```

---

## ☁️ Deploy to Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/donow-ai
gcloud run deploy donow-ai \
  --image gcr.io/YOUR_PROJECT_ID/donow-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

---

## 👩‍💻 Built By

*Puja Sinha* · CSE AI/ML · Vibe2Ship Hackathon 2026
