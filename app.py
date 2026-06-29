import streamlit as st
import google.generativeai as genai
import json
import re
import time
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = "PASTE KEY HERE"  # ← paste your key here

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DoNow — Stop Procrastinating",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f0f0f0;
}

.stApp {
    background: #0a0a0f;
    min-height: 100vh;
}

#MainMenu, footer, header, section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 2.5rem;
    border-bottom: 1px solid #1a1a2e;
    background: #0a0a0f;
    position: sticky;
    top: 0;
    z-index: 100;
}
.logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #fff;
}
.logo span { color: #ff4d4d; }
.time-display {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #444;
    letter-spacing: 0.05em;
}

/* ── HERO ── */
.hero {
    padding: 3rem 2.5rem 2rem;
    max-width: 900px;
    margin: 0 auto;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff4d4d;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #fff;
    margin-bottom: 1rem;
}
.hero-title .dim { color: #333; }
.hero-sub {
    font-size: 1rem;
    color: #555;
    font-weight: 400;
    line-height: 1.6;
    max-width: 500px;
}

/* ── STREAK BAR ── */
.streak-bar {
    margin: 0 2.5rem 2rem;
    max-width: 855px;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    gap: 1rem;
    align-items: stretch;
}
.streak-card {
    flex: 1;
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}
.streak-card.fire { border-color: #ff4d4d33; }
.streak-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    line-height: 1;
}
.streak-num.red { color: #ff4d4d; }
.streak-num.green { color: #00ff88; }
.streak-label {
    font-size: 0.72rem;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── MAIN CONTENT ── */
.content-wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 2.5rem 4rem;
}

/* ── SECTION LABEL ── */
.sec-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #333;
    margin-bottom: 0.6rem;
    margin-top: 2rem;
}

/* ── INPUT AREA ── */
.stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    resize: none !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #ff4d4d55 !important;
    box-shadow: 0 0 0 3px #ff4d4d11 !important;
}
.stTextArea textarea::placeholder { color: #333 !important; }

.stTextInput input {
    background: #0f0f1a !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.65rem 1.4rem !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}
div[data-testid="stHorizontalBlock"] .stButton:first-child > button {
    background: #ff4d4d !important;
    color: #fff !important;
}
div[data-testid="stHorizontalBlock"] .stButton:first-child > button:hover {
    background: #ff3333 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stHorizontalBlock"] .stButton:not(:first-child) > button {
    background: #0f0f1a !important;
    color: #555 !important;
    border: 1px solid #1a1a2e !important;
}
div[data-testid="stHorizontalBlock"] .stButton:not(:first-child) > button:hover {
    color: #888 !important;
    border-color: #333 !important;
}

/* ── TASK CARDS ── */
.task-card {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.7rem;
    position: relative;
    transition: border-color 0.2s, background 0.2s;
}
.task-card.active-task {
    border-color: #ff4d4d;
    background: #1a0a0a;
    box-shadow: 0 0 30px #ff4d4d15;
}
.task-card.done-task {
    opacity: 0.35;
    border-color: #00ff8822;
}
.task-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.5rem;
}
.task-name {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.3;
}
.task-name.done-text {
    text-decoration: line-through;
    color: #333;
}
.task-meta {
    display: flex;
    gap: 0.6rem;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 0.4rem;
}
.badge {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 6px;
}
.badge-critical { background: #ff4d4d22; color: #ff6b6b; border: 1px solid #ff4d4d33; }
.badge-high     { background: #ff8c0022; color: #ffa833; border: 1px solid #ff8c0033; }
.badge-medium   { background: #ffd70022; color: #ffd700; border: 1px solid #ffd70033; }
.badge-low      { background: #00ff8822; color: #00ff88; border: 1px solid #00ff8833; }
.badge-time     { background: #ffffff0a; color: #555; border: 1px solid #1a1a2e; }

.task-reason {
    font-size: 0.82rem;
    color: #444;
    margin-top: 0.5rem;
    line-height: 1.5;
}
.task-reason.active-reason { color: #888; }

/* Subtasks */
.subtasks {
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid #1a1a2e;
}
.subtask-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.25rem 0;
    font-size: 0.84rem;
    color: #555;
}
.subtask-dot { color: #ff4d4d; font-size: 0.6rem; }

/* ── FOCUS MODE ── */
.focus-banner {
    background: linear-gradient(135deg, #1a0505, #0f0f1a);
    border: 1px solid #ff4d4d44;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
}
.focus-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff4d4d;
    margin-bottom: 0.4rem;
}
.focus-task {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 0.3rem;
}
.focus-timer {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #ff4d4d;
    letter-spacing: -0.02em;
    margin: 0.5rem 0;
}
.focus-sub {
    font-size: 0.82rem;
    color: #444;
}

/* ── AI INSIGHT ── */
.insight-box {
    background: #0f0f1a;
    border-left: 3px solid #ff4d4d;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: #888;
    line-height: 1.7;
}
.insight-box strong { color: #fff; }

/* ── PROCRASTINATION ALERT ── */
.proc-alert {
    background: #1a0a0a;
    border: 1px solid #ff4d4d44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #ff6b6b;
    line-height: 1.6;
}

/* ── CHAT ── */
.chat-msg-user {
    text-align: right;
    margin: 0.5rem 0;
}
.chat-msg-user span {
    background: #ff4d4d22;
    border: 1px solid #ff4d4d33;
    border-radius: 14px 14px 2px 14px;
    padding: 0.6rem 1rem;
    color: #f0f0f0;
    display: inline-block;
    max-width: 80%;
    font-size: 0.9rem;
    text-align: left;
}
.chat-msg-ai {
    margin: 0.5rem 0;
}
.chat-msg-ai span {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 2px 14px 14px 14px;
    padding: 0.6rem 1rem;
    color: #888;
    display: inline-block;
    max-width: 80%;
    font-size: 0.9rem;
}

/* ── SCHEDULE ── */
.schedule-block {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.4rem;
    display: flex;
    gap: 1rem;
    align-items: center;
}
.schedule-time {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: #ff4d4d;
    min-width: 90px;
}
.schedule-desc {
    font-size: 0.88rem;
    color: #888;
}

/* ── PROGRESS BAR ── */
.progress-wrap {
    background: #1a1a2e;
    border-radius: 999px;
    height: 4px;
    margin: 0.5rem 0 1.2rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff4d4d, #ff8c00);
    transition: width 0.4s ease;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .topbar { padding: 1rem 1.2rem; }
    .hero { padding: 1.5rem 1.2rem 1rem; }
    .hero-title { font-size: 1.8rem; }
    .streak-bar { margin: 0 1.2rem 1.5rem; flex-wrap: wrap; }
    .streak-card { min-width: calc(50% - 0.5rem); }
    .content-wrap { padding: 0 1.2rem 3rem; }
    .streak-num { font-size: 1.4rem; }
    .focus-timer { font-size: 2rem; }
    .task-card, .active-task, .done-task { padding: 1rem; }
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 0.5rem !important;
    border-bottom: 1px solid #1a1a2e !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #333 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1rem !important;
    border-radius: 8px 8px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #fff !important;
    border-bottom: 2px solid #ff4d4d !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
defaults = {
    "tasks": [], "analyzed": False, "active_task_idx": None,
    "focus_start": None, "completed_today": 0, "total_today": 0,
    "chat_history": [], "schedule": "", "streak": 1,
    "ai_insight": "", "suggested_start": "", "focus_elapsed": 0,
    "proc_warning": ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── AI FUNCTIONS ──────────────────────────────────────────────────────────────
def ai_analyze(tasks_text: str, time_of_day: str) -> dict:
    prompt = f"""
You are DoNow — a blunt, no-nonsense AI built for a CS student who procrastinates by 
can't-start paralysis and social media distraction.

Current time: {datetime.now().strftime("%A %I:%M %p")} ({time_of_day})
Tasks entered:
{tasks_text}

Return ONLY valid JSON, no markdown:
{{
  "tasks": [
    {{
      "name": "exact task name",
      "priority": "Critical|High|Medium|Low",
      "estimated_minutes": <number>,
      "reason": "blunt 1-sentence reason why this priority NOW",
      "subtasks": ["very small concrete step 1", "step 2", "step 3"],
      "start_phrase": "exact first physical action to take in 10 words or less",
      "distraction_risk": "High|Medium|Low"
    }}
  ],
  "total_hours": <number>,
  "ai_insight": "2-3 sentences. Be direct. Name the real problem with THIS list. Don't be nice.",
  "suggested_start": "Name ONE task to start in next 60 seconds. Say exactly what to open/touch first.",
  "procrastination_warning": "If you see deadline risk, say it brutally. Otherwise empty string."
}}
"""
    try:
        resp = model.generate_content(prompt)
        text = re.sub(r"```json|```", "", resp.text).strip()
        return json.loads(text)
    except Exception as e:
        return {"error": str(e)}


def ai_coach(msg: str, tasks: list, active_task: str) -> str:
    task_summary = "\n".join([f"- {t['name']} ({t['priority']})" for t in tasks]) if tasks else "No tasks yet."
    prompt = f"""
You are DoNow coach — brutally honest, zero fluff. The user is a CS student who 
procrastinates badly (can't start tasks, gets distracted by social media).

Current tasks:
{task_summary}

Active task right now: {active_task or 'None - they have not started yet'}
Time: {datetime.now().strftime("%I:%M %p")}

User says: "{msg}"

Reply in 2-4 sentences max. Be direct. If they're avoiding work, call it out.
If they need help starting, give the ONE specific action. No bullet lists.
"""
    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {e}"


def ai_schedule(tasks: list, start_hour: int) -> str:
    task_data = json.dumps([{"name": t["name"], "minutes": t["estimated_minutes"], "priority": t["priority"]} for t in tasks])
    prompt = f"""
Create a tight Pomodoro schedule starting at {start_hour}:00.
Tasks: {task_data}

Rules:
- 25 min focus blocks
- 5 min breaks between blocks  
- 15 min break after every 2 hours
- Put Critical/High tasks first
- Be realistic about what fits

Format each line EXACTLY as:
HH:MM | Task name or Break
(nothing else, no headers, no explanation)
"""
    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {e}"


# ── TOPBAR ────────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""
<div class='topbar'>
  <div class='logo'>Do<span>Now</span></div>
  <div class='time-display'>{now.strftime("%a %I:%M %p").upper()}</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
hour = now.hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
urgency = "What are you waiting for?" if hour > 20 else "Every hour counts." if hour > 17 else "Make today count."

st.markdown(f"""
<div class='hero'>
  <div class='hero-eyebrow'>Anti-procrastination engine</div>
  <h1 class='hero-title'>{greeting}.<br><span class='dim'>{urgency}</span></h1>
  <p class='hero-sub'>Add your tasks. Get a brutal priority order. Start in 60 seconds or less.</p>
</div>
""", unsafe_allow_html=True)

# ── STREAK BAR ────────────────────────────────────────────────────────────────
completed = st.session_state.completed_today
total = st.session_state.total_today
pct = int((completed / total * 100)) if total > 0 else 0

st.markdown(f"""
<div class='streak-bar'>
  <div class='streak-card fire'>
    <div class='streak-num red'>{st.session_state.streak}</div>
    <div class='streak-label'>Day streak 🔥</div>
  </div>
  <div class='streak-card'>
    <div class='streak-num green'>{completed}</div>
    <div class='streak-label'>Done today</div>
  </div>
  <div class='streak-card'>
    <div class='streak-num'>{total - completed}</div>
    <div class='streak-label'>Remaining</div>
  </div>
  <div class='streak-card'>
    <div class='streak-num'>{pct}%</div>
    <div class='streak-label'>Day progress</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN CONTENT ──────────────────────────────────────────────────────────────
st.markdown("<div class='content-wrap'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔥 Tasks", "⏱ Focus Mode", "💬 Coach"])

# ═══════════════════════════════════════════════════
# TAB 1 — TASKS
# ═══════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='sec-label'>What do you need to get done today?</div>", unsafe_allow_html=True)

    tasks_input = st.text_area(
        "",
        placeholder="Type your tasks, one per line:\n\nFinish ML assignment due tonight\nReply to professor email\nStudy for Thursday quiz\nClean up GitHub portfolio\nRead 2 chapters of OS book",
        height=160,
        label_visibility="collapsed",
        key="tasks_input"
    )

    time_of_day = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        analyze_btn = st.button("🔥 Analyze — Let's Go", use_container_width=True)
    with c2:
        clear_btn = st.button("Clear all", use_container_width=True)
    with c3:
        refresh_btn = st.button("Re-analyze", use_container_width=True)

    if clear_btn:
        st.session_state.tasks = []
        st.session_state.analyzed = False
        st.session_state.active_task_idx = None
        st.session_state.completed_today = 0
        st.session_state.total_today = 0
        st.session_state.schedule = ""
        st.rerun()

    if analyze_btn or refresh_btn:
        text = tasks_input.strip()
        if not text:
            st.warning("Add at least one task first.")
        else:
            with st.spinner("Analyzing..."):
                result = ai_analyze(text, time_of_day)
            if "error" in result:
                st.error(f"AI Error: {result['error']}")
            else:
                st.session_state.tasks = result.get("tasks", [])
                st.session_state.ai_insight = result.get("ai_insight", "")
                st.session_state.suggested_start = result.get("suggested_start", "")
                st.session_state.proc_warning = result.get("procrastination_warning", "")
                st.session_state.total_today = len(st.session_state.tasks)
                st.session_state.analyzed = True
                st.session_state.schedule = ""
                st.rerun()

    # ── Results ──
    if st.session_state.analyzed and st.session_state.tasks:

        # Progress bar
        pct2 = int(st.session_state.completed_today / len(st.session_state.tasks) * 100) if st.session_state.tasks else 0
        st.markdown(f"""
        <div class='progress-wrap'>
          <div class='progress-fill' style='width:{pct2}%'></div>
        </div>
        """, unsafe_allow_html=True)

        # Procrastination warning
        if st.session_state.proc_warning:
            st.markdown(f"<div class='proc-alert'>⚠️ {st.session_state.proc_warning}</div>", unsafe_allow_html=True)

        # AI Insight
        if st.session_state.ai_insight:
            st.markdown(f"<div class='insight-box'>{st.session_state.ai_insight}</div>", unsafe_allow_html=True)

        # Start now box
        if st.session_state.suggested_start:
            st.markdown(f"""
            <div style='background:#1a0505; border:1px solid #ff4d4d55; border-radius:12px; 
            padding:1rem 1.2rem; margin-bottom:1rem;'>
              <div style='font-size:0.65rem; color:#ff4d4d; font-weight:700; letter-spacing:0.15em; 
              text-transform:uppercase; margin-bottom:0.3rem;'>Start right now →</div>
              <div style='font-size:0.95rem; color:#fff; font-weight:600;'>{st.session_state.suggested_start}</div>
            </div>
            """, unsafe_allow_html=True)

        # Confetti when all tasks done
        all_done = all(t.get("done", False) for t in st.session_state.tasks) and len(st.session_state.tasks) > 0
        if all_done:
            st.balloons()
            st.markdown("""
            <div style='background:linear-gradient(135deg,#0a1a0a,#0f0f1a); border:1px solid #00ff8844;
            border-radius:16px; padding:2rem; text-align:center; margin-bottom:1rem;'>
              <div style='font-size:2.5rem;'>🎉</div>
              <div style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:#00ff88; margin:0.5rem 0;'>
                You crushed it today!
              </div>
              <div style='color:#555; font-size:0.9rem;'>Every single task — done. This is what discipline looks like.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='sec-label'>Priority order</div>", unsafe_allow_html=True)

        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(
            enumerate(st.session_state.tasks),
            key=lambda x: priority_order.get(x[1]["priority"], 4)
        )

        for orig_idx, task in sorted_tasks:
            is_done = task.get("done", False)
            is_active = st.session_state.active_task_idx == orig_idx
            p = task["priority"].lower()

            card_class = "done-task" if is_done else ("active-task" if is_active else "task-card")
            name_class = "task-name done-text" if is_done else "task-name"
            reason_class = "task-reason active-reason" if is_active else "task-reason"

            st.markdown(f"""
            <div class='{card_class}'>
              <div class='task-header'>
                <div class='{name_class}'>{task['name']}</div>
              </div>
              <div class='task-meta'>
                <span class='badge badge-{p}'>{task['priority']}</span>
                <span class='badge badge-time'>⏱ {task['estimated_minutes']} min</span>
                {'<span class="badge badge-critical">📱 Distraction risk</span>' if task.get('distraction_risk') == 'High' else ''}
                {'<span class="badge" style="background:#ff4d4d22;color:#ff4d4d;border:1px solid #ff4d4d33;">● ACTIVE</span>' if is_active else ''}
                
              </div>
              <div class='{reason_class}'>{task.get('reason', '')}</div>
              {'<div style="margin-top:0.5rem; background:#ff4d4d11; border-radius:8px; padding:0.5rem 0.8rem; font-size:0.82rem; color:#ff6b6b;"><strong>Start by:</strong> ' + task.get('start_phrase', '') + '</div>' if is_active and task.get('start_phrase') else ''}
            </div>
            """, unsafe_allow_html=True)

            if not is_done:
                b1, b2, b3 = st.columns([2, 1, 1])
                with b1:
                    if not is_active:
                        if st.button(f"▶ Start this", key=f"start_{orig_idx}", use_container_width=True):
                            st.session_state.active_task_idx = orig_idx
                            st.session_state.focus_start = time.time()
                            st.rerun()
                    else:
                        if st.button(f"⏸ Pause", key=f"pause_{orig_idx}", use_container_width=True):
                            st.session_state.active_task_idx = None
                            st.rerun()
                with b2:
                    if st.button(f"✓ Done", key=f"done_{orig_idx}", use_container_width=True):
                        st.session_state.tasks[orig_idx]["done"] = True
                        st.session_state.completed_today += 1
                        if st.session_state.active_task_idx == orig_idx:
                            st.session_state.active_task_idx = None
                        st.rerun()
                with b3:
                    with st.expander("Steps"):
                        for sub in task.get("subtasks", []):
                            st.markdown(f"<div class='subtask-row'><span class='subtask-dot'>◆</span>{sub}</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 2 — FOCUS MODE
# ═══════════════════════════════════════════════════
with tab2:
    if st.session_state.active_task_idx is not None:
        idx = st.session_state.active_task_idx
        if idx < len(st.session_state.tasks):
            task = st.session_state.tasks[idx]

            # Calculate elapsed
            elapsed = 0
            if st.session_state.focus_start:
                elapsed = int(time.time() - st.session_state.focus_start)

            mins = elapsed // 60
            secs = elapsed % 60

            # Pomodoro: 25 min = 1500 seconds
            pomodoro_remaining = max(0, 1500 - elapsed)
            p_mins = pomodoro_remaining // 60
            p_secs = pomodoro_remaining % 60

            st.markdown(f"""
            <div class='focus-banner'>
              <div class='focus-title'>🔥 Focus mode — put your phone down</div>
              <div class='focus-task'>{task['name']}</div>
              <div class='focus-timer'>{p_mins:02d}:{p_secs:02d}</div>
              <div class='focus-sub'>Pomodoro remaining &nbsp;·&nbsp; {mins}m {secs}s elapsed</div>
            </div>
            """, unsafe_allow_html=True)

            # Phone lock reminder
            if elapsed > 0 and elapsed % 300 == 0:
                st.markdown("<div class='proc-alert'>📵 Still on track? Phone face-down. Stay focused.</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='insight-box'>
              <strong>Start phrase:</strong> {task.get('start_phrase', 'Open your notes and write the first sentence.')}
            </div>
            """, unsafe_allow_html=True)

            # Subtasks as checklist
            st.markdown("<div class='sec-label'>Break it down</div>", unsafe_allow_html=True)
            for i, sub in enumerate(task.get("subtasks", [])):
                st.checkbox(sub, key=f"focus_sub_{idx}_{i}")

            fc1, fc2 = st.columns(2)
            with fc1:
                if st.button("✓ Mark complete", use_container_width=True):
                    st.session_state.tasks[idx]["done"] = True
                    st.session_state.completed_today += 1
                    st.session_state.active_task_idx = None
                    st.session_state.focus_start = None
                    st.rerun()
            with fc2:
                if st.button("⏸ Stop focus", use_container_width=True):
                    st.session_state.active_task_idx = None
                    st.rerun()

            # Auto-refresh every 30s to update timer
            time.sleep(0.1)
            st.rerun()

    else:
        st.markdown("""
        <div style='text-align:center; padding:4rem 2rem; color:#333;'>
          <div style='font-size:3rem; margin-bottom:1rem;'>⏱</div>
          <div style='font-family:Syne,sans-serif; font-size:1.1rem; font-weight:700; color:#444;'>No active task</div>
          <div style='font-size:0.85rem; margin-top:0.4rem;'>Go to Tasks tab → hit Start on a task → come back here</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.tasks:
            st.markdown("<div class='sec-label'>Quick start</div>", unsafe_allow_html=True)
            pending = [(i, t) for i, t in enumerate(st.session_state.tasks) if not t.get("done")]
            if pending:
                priority_order2 = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
                pending.sort(key=lambda x: priority_order2.get(x[1]["priority"], 4))
                top_idx, top_task = pending[0]
                st.markdown(f"""
                <div style='background:#1a0505; border:1px solid #ff4d4d44; border-radius:12px; 
                padding:1rem 1.2rem; margin-bottom:1rem;'>
                  <div style='font-size:0.7rem; color:#ff4d4d; letter-spacing:0.15em; margin-bottom:0.3rem;'>MOST URGENT</div>
                  <div style='font-size:1rem; font-weight:700; color:#fff;'>{top_task['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"▶ Start now — {top_task['name'][:30]}", use_container_width=True):
                    st.session_state.active_task_idx = top_idx
                    st.session_state.focus_start = time.time()
                    st.rerun()

        # Schedule generator
        st.markdown("<div class='sec-label'>Generate today's schedule</div>", unsafe_allow_html=True)
        start_h = st.selectbox("Work starts at", [f"{h}:00 {'AM' if h < 12 else 'PM'}" for h in range(7, 23)], index=2)
        if st.button("Generate schedule", use_container_width=True):
            if not st.session_state.tasks:
                st.warning("Add and analyze tasks first.")
            else:
                with st.spinner("Building schedule..."):
                    h_val = int(start_h.split(":")[0])
                    st.session_state.schedule = ai_schedule(st.session_state.tasks, h_val)
                st.rerun()

        if st.session_state.schedule:
            st.markdown("<div class='sec-label'>Your schedule</div>", unsafe_allow_html=True)
            for line in st.session_state.schedule.split("\n"):
                if "|" in line:
                    parts = line.split("|", 1)
                    t_str = parts[0].strip()
                    d_str = parts[1].strip() if len(parts) > 1 else ""
                    is_break = "break" in d_str.lower()
                    st.markdown(f"""
                    <div class='schedule-block' style='{"opacity:0.4;" if is_break else ""}'>
                      <div class='schedule-time'>{t_str}</div>
                      <div class='schedule-desc'>{d_str}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# TAB 3 — COACH
# ═══════════════════════════════════════════════════
with tab3:
    active_name = ""
    if st.session_state.active_task_idx is not None:
        idx = st.session_state.active_task_idx
        if idx < len(st.session_state.tasks):
            active_name = st.session_state.tasks[idx]["name"]

    st.markdown("""
    <div class='insight-box' style='margin-bottom:1.5rem;'>
      <strong>DoNow Coach</strong> — I'm direct, I don't sugarcoat, and I will call out your excuses. 
      Ask me anything about your tasks, focus, or motivation.
    </div>
    """, unsafe_allow_html=True)

    # Quick triggers
    st.markdown("<div class='sec-label'>Quick actions</div>", unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    quick_map = {
        "I can't start": "I can't start any of my tasks. What do I do right now?",
        "I'm distracted": "I keep getting distracted by my phone. Help me focus.",
        "What's most urgent?": "Looking at my tasks, what's most urgent and why?"
    }
    for col, (label, prompt_text) in zip([q1, q2, q3], quick_map.items()):
        with col:
            if st.button(label, use_container_width=True, key=f"quick_{label}"):
                with st.spinner("..."):
                    reply = ai_coach(prompt_text, st.session_state.tasks, active_name)
                st.session_state.chat_history.append({"role": "user", "content": prompt_text})
                st.session_state.chat_history.append({"role": "ai", "content": reply})
                st.rerun()

    st.markdown("<div class='sec-label'>Chat</div>", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.chat_history[-10:]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-msg-user'><span>{msg['content']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-msg-ai'><span>{msg['content']}</span></div>", unsafe_allow_html=True)

    # Input
    ci1, ci2 = st.columns([5, 1])
    with ci1:
        user_msg = st.text_input("", placeholder="Ask your coach...", key="coach_input", label_visibility="collapsed")
    with ci2:
        send = st.button("Send", use_container_width=True, key="coach_send")

    if send and user_msg.strip():
        with st.spinner("..."):
            reply = ai_coach(user_msg, st.session_state.tasks, active_name)
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        st.session_state.chat_history.append({"role": "ai", "content": reply})
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
