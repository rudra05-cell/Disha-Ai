"""
DISHA AI — server.py (with concurrent user handling)
Run: python server.py
Open: http://localhost:8080
"""
import asyncio, json, os, time, uuid
from datetime import datetime
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from google.genai.errors import ClientError
from disha_agent.agent import root_agent

# ── App Setup ─────────────────────────────────────────────────────────────────
app = FastAPI(title="Disha AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

MEMORY_PATH = Path("disha_agent/memory_store")
MEMORY_PATH.mkdir(parents=True, exist_ok=True)
JOURNAL = MEMORY_PATH / "student_journal.json"

active_sessions: dict = {}

# Global lock — only ONE AI call at a time on free tier
# This prevents quota exhaustion when multiple users connect
api_lock = asyncio.Lock()

# ── Models ────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    session_id: str
    message: str

# ── Memory ────────────────────────────────────────────────────────────────────
def read_journal():
    if JOURNAL.exists():
        with open(JOURNAL) as f: return json.load(f)
    return {"sessions": []}

def save_session(sid, notes):
    j = read_journal()
    j["sessions"].append({
        "session_id": sid,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notes": notes
    })
    with open(JOURNAL, "w") as f: json.dump(j, f, indent=2)

# ── API ───────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    active = len(active_sessions)
    locked = api_lock.locked()
    return {
        "status": "ok",
        "active_sessions": active,
        "api_busy": locked,
        "message": "Disha is helping someone right now. Please wait." if locked else "Ready"
    }

@app.post("/api/session/new")
async def new_session():
    sid = str(uuid.uuid4())
    svc = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="disha_ai", session_service=svc)
    await svc.create_session(
        app_name="disha_ai", user_id="student", session_id=sid
    )
    active_sessions[sid] = {"runner": runner, "svc": svc, "turns": 0}
    return {"session_id": sid}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if req.session_id not in active_sessions:
        raise HTTPException(404, "Session not found. Start a new session.")

    data = active_sessions[req.session_id]
    runner = data["runner"]
    data["turns"] += 1

    async def stream():
        # Try to acquire the API lock
        # If another conversation is active, notify this user to wait
        if api_lock.locked():
            yield f"data: {json.dumps({'type':'status','text':'Disha is finishing with another student. Your turn is next — please wait 30 seconds...'})}\n\n"
            # Wait up to 120 seconds for the lock
            waited = 0
            while api_lock.locked() and waited < 120:
                await asyncio.sleep(2)
                waited += 2
                if waited % 10 == 0:
                    yield f"data: {json.dumps({'type':'status','text':f'Almost your turn... ({120-waited}s)'})}\n\n"

        async with api_lock:
            try:
                msg = genai_types.Content(
                    role="user",
                    parts=[genai_types.Part(text=req.message)]
                )
                collected = []
                last_author = "disha"

                for attempt in range(1, 4):
                    try:
                        async for event in runner.run_async(
                            user_id="student",
                            session_id=req.session_id,
                            new_message=msg
                        ):
                            if not event.content or not event.content.parts:
                                continue
                            text = "".join(
                                p.text for p in event.content.parts
                                if hasattr(p, "text") and p.text
                            )
                            if text.strip():
                                last_author = getattr(event, "author", "disha")
                                collected.append(text.strip())
                                yield f"data: {json.dumps({'type':'chunk','text':text.strip(),'agent':last_author})}\n\n"
                        break

                    except ClientError as e:
                        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                            import re
                            match = re.search(r"(\d+)s", str(e))
                            wait = int(match.group(1)) + 5 if match else 35 * attempt
                            wait = min(wait, 90)
                            yield f"data: {json.dumps({'type':'status','text':f'Rate limit hit. Auto-retrying in {wait}s...'})}\n\n"
                            await asyncio.sleep(wait)
                        else:
                            raise

                combined = " ".join(collected).lower()
                done = any(s in combined for s in [
                    "hamesha yahan hai", "always here", "aa jaana"
                ])
                if done:
                    save_session(
                        req.session_id,
                        f"Completed in {data['turns']} turns."
                    )
                yield f"data: {json.dumps({'type':'done','is_complete':done,'agent':last_author})}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type':'error','text':str(e)[:150]})}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.get("/api/memory")
def memory():
    return read_journal()

@app.delete("/api/session/{sid}")
def end(sid: str):
    active_sessions.pop(sid, None)
    return {"ok": True}

# ── Frontend ──────────────────────────────────────────────────────────────────
static_path = Path("static")
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    p = Path("static/index.html")
    return HTMLResponse(
        p.read_text(encoding="utf-8") if p.exists()
        else "<h1>Disha AI — Static files not found</h1>"
    )

# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("\n  ERROR: GOOGLE_API_KEY not found in .env file")
        print("  Get free key: https://aistudio.google.com/apikey\n")
        exit(1)

    port = int(os.environ.get("PORT", 8080))
    print(f"\n  🧭 DISHA AI starting at http://localhost:{port}")
    print(f"  Free tier: one conversation at a time (queue enabled)\n")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")
