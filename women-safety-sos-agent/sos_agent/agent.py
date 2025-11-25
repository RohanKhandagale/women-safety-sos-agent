from google.adk.agents import Agent
import vertexai
import os
import json
import time
from pathlib import Path

vertexai.init(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"]
)

OUT_DIR = Path("sos_demo_outputs")
OUT_DIR.mkdir(exist_ok=True)

HELP_KEYWORDS = [
    "help", "save", "danger", "unsafe", "kidnap", "attack",
    "bachao", "madad", "खतरा", "अपहरण", "हमला", "मदद", "सुरक्षित नहीं"
]

def now_str():
    return time.strftime("%Y%m%d_%H%M%S")

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# -------- TOOLS --------

def transcribe_audio_tool(audio_file_url: str) -> dict:
    return {
        "status": "ok",
        "transcript": f"[Placeholder transcript for {audio_file_url}]",
        "audio_url": audio_file_url
    }

def detect_emergency_tool(text: str) -> dict:
    text_low = text.lower()
    matches = [w for w in HELP_KEYWORDS if w in text_low]

    if not matches:
        return {"is_emergency": False, "level": "none", "matches": []}

    level = "critical" if any(x in text_low for x in ["kidnap", "attack"]) else "danger"

    return {
        "is_emergency": True,
        "level": level,
        "matches": matches
    }

def confirm_sos_tool(prompt: str) -> dict:
    return {"confirmation_prompt": prompt}

def send_sos_simulated_tool(details: dict) -> dict:
    record = {
        "time": now_str(),
        "details": details,
        "note": "SOS simulated — no real dispatch."
    }
    file = OUT_DIR / f"sos_{now_str()}.json"
    save_json(record, file)
    return {"status": "ok", "saved_to": str(file)}

def memory_store_tool(event: dict) -> dict:
    file = OUT_DIR / "memory_log.json"
    if file.exists():
        data = json.load(open(file, "r"))
    else:
        data = []
    data.append(event)
    save_json(data, file)
    return {"status": "ok", "memory_file": str(file)}

# -------- AGENT --------

root_agent = Agent(
    name="women_safety_sos_agent",
    model="gemini-2.5-flash-lite",
    description="Multilingual SOS agent for women's safety.",
    instruction="""
You are a multilingual Women's Safety SOS Agent.

Rules:
- Understand ANY language.
- Always reply in the SAME language the user used.
- If danger is detected, call the detect_emergency_tool first.
- If an emergency exists → call confirm_sos_tool.
- After confirmation → call send_sos_simulated_tool.
- Store event using memory_store_tool.
- Be calming, short, supporting.
""",
    tools=[
        transcribe_audio_tool,
        detect_emergency_tool,
        confirm_sos_tool,
        send_sos_simulated_tool,
        memory_store_tool
    ]
)
