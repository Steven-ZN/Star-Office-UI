#!/usr/bin/env python3
"""Star Office UI - Backend State Service"""

from flask import Flask, jsonify, send_from_directory, request
from datetime import datetime
import json
import os
import subprocess

# Paths
ROOT_DIR = "/home/steven/clawd/Star-Office-UI"
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
STATE_FILE = os.path.join(ROOT_DIR, "state.json")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="/static")

# Default state
DEFAULT_STATE = {
    "state": "idle",
    "detail": "等待任务中...",
    "progress": 0,
    "updated_at": datetime.now().isoformat()
}


def load_state():
    """Load state from file.

    Includes a simple auto-idle mechanism:
    - If the last update is older than ttl_seconds (default 25s)
      and the state is a "working" state, we fall back to idle.

    This avoids the UI getting stuck at the desk when no new updates arrive.
    """
    state = None
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = None

    if not isinstance(state, dict):
        state = dict(DEFAULT_STATE)

    # Auto-idle
    try:
        ttl = int(state.get("ttl_seconds", 25))
        updated_at = state.get("updated_at")
        s = state.get("state", "idle")
        working_states = {"writing", "researching", "executing"}
        if updated_at and s in working_states:
            # tolerate both with/without timezone
            dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            # Use UTC for aware datetimes; local time for naive.
            if dt.tzinfo:
                from datetime import timezone
                age = (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()
            else:
                age = (datetime.now() - dt).total_seconds()
            if age > ttl:
                state["state"] = "idle"
                state["detail"] = "待命中（自动回到休息区）"
                state["progress"] = 0
                state["updated_at"] = datetime.now().isoformat()
                # persist the auto-idle so every client sees it consistently
                try:
                    save_state(state)
                except Exception:
                    pass
    except Exception:
        pass

    return state


def save_state(state: dict):
    """Save state to file"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True, timeout=6)
        out = (res.stdout or "") + ("\n" + res.stderr if res.stderr else "")
        return out.strip()
    except Exception as e:
        return f"[error] {e}"


# Initialize state
if not os.path.exists(STATE_FILE):
    save_state(DEFAULT_STATE)


@app.route("/", methods=["GET"])
def index():
    """Serve the pixel office UI"""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/status", methods=["GET"])
def get_status():
    """Get current state"""
    state = load_state()
    return jsonify(state)


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/set_state", methods=["POST"])
def set_state():
    data = request.get_json(silent=True) or {}
    state = load_state()
    if "state" in data:
        state["state"] = data["state"]
    if "detail" in data:
        state["detail"] = data["detail"]
    if "progress" in data:
        state["progress"] = data["progress"]
    state["updated_at"] = datetime.now().isoformat()
    save_state(state)
    return jsonify({"ok": True, "state": state})


@app.route("/gateway_logs", methods=["GET"])
def gateway_logs():
    """Fetch gateway logs"""
    text = run_cmd("openclaw logs --limit 120 --plain --no-color --timeout 8000")
    return jsonify({"text": text})


@app.route("/tui", methods=["GET"])
def tui():
    """Fetch TUI/status output"""
    text = run_cmd("openclaw status --deep")
    return jsonify({"text": text})


if __name__ == "__main__":
    print("=" * 50)
    print("Star Office UI - Backend State Service")
    print("=" * 50)
    print(f"State file: {STATE_FILE}")
    print("Listening on: http://0.0.0.0:18791")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=18791, debug=False)
