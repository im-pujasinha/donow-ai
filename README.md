# 🔥 DoNow — Stop Procrastinating

> An AI-powered anti-procrastination engine built for students who can't start tasks and get distracted by social media.

**Vibe2Ship Hackathon** · Problem Statement: The Last-Minute Life Saver

---

## 🚀 Live Demo
[Deployed on Streamlit Cloud] → *(add link after deployment)*

---

## 🎯 Problem

Students miss deadlines not because they don't know what to do — but because they **can't start**, and **social media pulls them away** the moment they try. Generic task apps just list tasks. DoNow actively fights procrastination.

---

## Problem It Solves

Students, professionals, and entrepreneurs constantly miss deadlines because existing productivity tools rely on passive reminders that are easy to ignore. DoNow solves this by directly targeting the two biggest causes of procrastination: the inability to start a task, and distraction from social media. It uses Google Gemini AI to break down every task into a concrete first action, flags which tasks carry the highest distraction risk, and locks the user into a Pomodoro-based focus mode with phone-down reminders until the task is done.

---

## Challenges Faced

The biggest challenge was designing AI prompts that produced genuinely actionable output rather than generic advice. Early prompt versions returned vague suggestions like "prioritize your tasks," which did not help with the user's actual problem of not knowing how to begin. The prompts were refined to force the AI to output a specific first physical action for every task, along with a distraction risk rating, making the guidance concrete rather than abstract. Another challenge was handling Gemini API rate limits gracefully so the app stays usable even when the free tier quota is reached, which was solved by adding friendly fallback messages instead of raw error output.

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
- **Streamlit** — UI framework and deployment (Streamlit Community Cloud)
- **Google Gemini 2.5 Flash** — AI core (prioritization, coaching, scheduling)

---

## 🔧 Google Technologies

- **Gemini 2.5 Flash API** — Task analysis, schedule generation, AI coaching
- **Google AI Studio** — Model access and API key management

---

## 🏃 Run Locally

```bash
git clone https://github.com/im-pujasinha/donow-ai
cd donow-ai
pip install -r requirements.txt
streamlit run app.py
```

---

## 👩‍💻 Built By

*Puja Sinha* · CSE AI/ML · Vibe2Ship Hackathon 2026
