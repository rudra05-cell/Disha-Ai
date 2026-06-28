"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     DISHA AI — Streamlit Frontend (app.py)                ║
║                                                                              ║
║  This is the visual interface judges see in the demo video.                ║
║  Run with: streamlit run app.py                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── ADK 2.0 Runtime Imports ───────────────────────────────────────────────────
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

# ── Import our Disha workflow ─────────────────────────────────────────────────
from disha_agent.agent import root_agent, MEMORY_STORE_PATH

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Disha AI — Your Life Navigation Companion",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — makes it look professional for the demo video
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }

    /* Hide default streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero section */
    .hero-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: white;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.85);
        margin-top: 8px;
    }
    .hero-stat {
        background: rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 10px 16px;
        display: inline-block;
        margin: 6px;
        font-size: 0.9rem;
        color: white;
    }

    /* Stage selector */
    .stage-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.2s;
        color: white;
    }
    .stage-card:hover {
        background: rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.6);
    }

    /* Chat messages */
    .disha-msg {
        background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
        border: 1px solid rgba(102,126,234,0.3);
        border-radius: 16px 16px 16px 4px;
        padding: 16px 20px;
        margin: 10px 0;
        color: #e8e8f0;
        font-size: 1rem;
        line-height: 1.6;
    }
    .user-msg {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px 16px 4px 16px;
        padding: 14px 20px;
        margin: 10px 0;
        color: #e8e8f0;
        text-align: right;
        font-size: 1rem;
    }
    .agent-label {
        font-size: 0.75rem;
        color: rgba(102,126,234,0.9);
        font-weight: 600;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 10px;
        margin: 16px 0;
        flex-wrap: wrap;
    }
    .stat-pill {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 0.8rem;
        color: rgba(255,255,255,0.7);
    }

    /* Input area */
    .stTextArea textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(102,126,234,0.4) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 1rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* Memory panel */
    .memory-box {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.75);
    }
    .memory-title {
        color: #4ade80;
        font-weight: 600;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    /* Thinking spinner */
    .thinking-box {
        background: rgba(102,126,234,0.1);
        border: 1px solid rgba(102,126,234,0.25);
        border-radius: 12px;
        padding: 16px 20px;
        color: rgba(255,255,255,0.6);
        font-size: 0.95rem;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────

def init_session():
    """Initialise all Streamlit session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []  # List of {role, content, agent}
    if "adk_session_service" not in st.session_state:
        st.session_state.adk_session_service = InMemorySessionService()
    if "adk_session_created" not in st.session_state:
        st.session_state.adk_session_created = False
    if "runner" not in st.session_state:
        st.session_state.runner = Runner(
            agent=root_agent,
            app_name="disha_ai",
            session_service=st.session_state.adk_session_service,
        )
    if "past_sessions" not in st.session_state:
        st.session_state.past_sessions = load_past_sessions()
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = None


def load_past_sessions() -> list:
    """Load past sessions from MCP memory store for display."""
    journal_path = Path(MEMORY_STORE_PATH) / "student_journal.json"
    if journal_path.exists():
        try:
            with open(journal_path) as f:
                data = json.load(f)
                return data.get("sessions", [])
        except Exception:
            return []
    return []


# ─────────────────────────────────────────────────────────────────────────────
# ADK RUNNER — Async execution
# ─────────────────────────────────────────────────────────────────────────────

async def create_adk_session():
    """Create ADK session if not already created."""
    if not st.session_state.adk_session_created:
        await st.session_state.adk_session_service.create_session(
            app_name="disha_ai",
            user_id="student_001",
            session_id=st.session_state.session_id,
        )
        st.session_state.adk_session_created = True


async def run_disha(user_message: str) -> list[dict]:
    """
    Run the Disha ADK workflow with a user message.
    Returns list of {agent, text} response dicts from all nodes.
    """
    await create_adk_session()

    message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=user_message)],
    )

    responses = []
    async for event in st.session_state.runner.run_async(
        user_id="student_001",
        session_id=st.session_state.session_id,
        new_message=message,
    ):
        if not event.content or not event.content.parts:
            continue
        text = "".join(
            p.text for p in event.content.parts
            if hasattr(p, "text") and p.text
        )
        if text.strip():
            author = getattr(event, "author", "disha")
            # Clean up agent names for display
            display_names = {
                "life_stage_detector": "🎯 Disha — Getting to know you",
                "interest_discovery":  "💡 Disha — Discovering your interests",
                "india_navigator":     "🔍 Disha — Searching real opportunities",
                "path_architect":      "🗺️ Disha — Designing your paths",
                "first_step_coach":    "🚀 Disha — Your first step",
                "disha_ai":            "🧭 Disha AI",
            }
            display_name = display_names.get(author, "🧭 Disha")
            responses.append({"agent": display_name, "text": text})

    return responses


def run_async(coro):
    """Run async coroutine from Streamlit's sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


# ─────────────────────────────────────────────────────────────────────────────
# UI RENDERING
# ─────────────────────────────────────────────────────────────────────────────

def render_hero():
    """Render the top hero section."""
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🧭 Disha AI</div>
        <div class="hero-subtitle">
            The life companion every Indian student deserves at every crossroads.
        </div>
        <div style="margin-top: 16px;">
            <span class="hero-stat">📊 9 in 10 students have NO guidance</span>
            <span class="hero-stat">🆓 Completely Free</span>
            <span class="hero-stat">🔒 Your data stays local</span>
            <span class="hero-stat">🧠 Remembers you across sessions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_past_sessions():
    """Show past sessions panel if they exist."""
    sessions = load_past_sessions()
    if sessions:
        with st.expander(f"📖 Your Journey — {len(sessions)} past session(s)", expanded=False):
            for i, s in enumerate(sessions[-3:], 1):  # Show last 3
                st.markdown(f"""
                <div class="memory-box">
                    <div class="memory-title">🗓️ Session {i} — {s.get('date', 'Unknown date')}</div>
                    <strong>Stage:</strong> {s.get('life_stage', '?')} &nbsp;|&nbsp;
                    <strong>Interest found:</strong> {s.get('interest_revealed', '?')}<br>
                    <strong>Path recommended:</strong> {s.get('recommendation_given', '?')}<br>
                    <strong>Your first step was:</strong> {s.get('first_step_assigned', '?')}
                </div>
                """, unsafe_allow_html=True)


def render_messages():
    """Render all chat messages."""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="user-msg">{msg["content"]}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="agent-label">{msg.get("agent", "🧭 Disha")}</div>
            <div class="disha-msg">{msg["content"]}</div>
            """, unsafe_allow_html=True)


def render_stage_selector():
    """Show quick-start buttons for different life stages."""
    st.markdown("### 🌟 Where are you in life right now?")
    st.markdown("*Tap your current stage, or type freely below*")

    stages = [
        ("📚 Just finished Class 10",
         "Maine abhi 10th complete ki hai aur mujhe samajh nahi aa raha ki aage kya karoon — Science loon, Commerce loon, ya kuch aur?"),
        ("🎓 Just finished Class 12",
         "Maine 12th complete ki hai. JEE/NEET ka result aaya hai. Ab college admission aur career ke baare mein confused hoon."),
        ("🏫 Currently in College (BE/BTech/BSc etc.)",
         "Main college mein hoon, final year ya beech mein. Placement ka pressure hai. GATE karoon, job karoon, ya kuch aur?"),
        ("😕 Graduated but LOST — no direction",
         "Maine graduation kar li hai par kuch samajh nahi aa raha. Koi clear direction nahi hai, stress bahut hai."),
        ("❓ I have NO idea what I'm interested in",
         "Mujhe honestly nahi pata mujhe kya pasand hai ya kya karna chahta/chahti hoon. Sab confusing lagta hai."),
    ]

    cols = st.columns(1)
    for label, message in stages:
        if st.button(label, key=f"stage_{label}"):
            st.session_state.current_stage = message
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    init_session()

    # Check API key
    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        st.error(
            "⚠️ GOOGLE_API_KEY not found. "
            "Get your free key at https://aistudio.google.com/apikey "
            "and add it to your .env file."
        )
        st.stop()

    # Hero
    render_hero()

    # Past sessions
    render_past_sessions()

    # If no messages yet, show stage selector
    if not st.session_state.messages:
        render_stage_selector()
        st.markdown("---")

    # Render conversation
    render_messages()

    # Handle pre-selected stage (from buttons)
    if st.session_state.current_stage:
        user_input = st.session_state.current_stage
        st.session_state.current_stage = None

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })

        # Run Disha workflow
        with st.spinner("Disha soch rahi hai... 🧭"):
            responses = run_async(run_disha(user_input))

        for r in responses:
            st.session_state.messages.append({
                "role": "assistant",
                "agent": r["agent"],
                "content": r["text"],
            })

        st.rerun()

    # Text input for follow-up
    st.markdown("---")
    user_text = st.text_area(
        "Apni baat yahan likho (Write your question here):",
        placeholder="Koi bhi sawaal poochho — Hindi ya English mein...",
        height=80,
        key="user_input_box",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        send = st.button("Disha se baat karo 🧭", use_container_width=True)
    with col2:
        if st.button("🔄 Naya shuru", use_container_width=True):
            for key in ["messages", "adk_session_created", "session_id",
                        "runner", "adk_session_service"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    if send and user_text.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_text,
        })

        with st.spinner("Disha soch rahi hai... 🧭"):
            responses = run_async(run_disha(user_text))

        for r in responses:
            st.session_state.messages.append({
                "role": "assistant",
                "agent": r["agent"],
                "content": r["text"],
            })

        st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align:center; margin-top:32px; color:rgba(255,255,255,0.3);
                font-size:0.8rem;">
        🧭 Disha AI — Built for Kaggle/Google AI Agents Intensive Capstone 2026<br>
        Agents for Good Track · ADK 2.0 · MCP · Antigravity · Gemini 2.5 Flash<br>
        <em>"We built the tool we needed and never had."</em>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
