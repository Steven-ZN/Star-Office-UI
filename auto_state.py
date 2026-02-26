#!/usr/bin/env python3
import os, time, json
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
SESSIONS_DIR = os.path.expanduser("/home/steven/.openclaw/agents/main/sessions")
CHECK_INTERVAL = 5  # seconds
ACTIVE_WINDOW = 20  # seconds

DEFAULT_STATE = {
    "state": "idle",
    "detail": "等待任务中...",
    "progress": 0,
    "updated_at": datetime.now().isoformat()
}


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return dict(DEFAULT_STATE)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def latest_session_mtime():
    latest = 0
    if not os.path.isdir(SESSIONS_DIR):
        return 0
    for name in os.listdir(SESSIONS_DIR):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(SESSIONS_DIR, name)
        try:
            mtime = os.path.getmtime(path)
            if mtime > latest:
                latest = mtime
        except Exception:
            pass
    return latest


def main():
    last_state = None
    while True:
        now = time.time()
        latest = latest_session_mtime()
        active = (now - latest) <= ACTIVE_WINDOW if latest > 0 else False

        state = load_state()
        if active:
            desired = "writing"
            detail = "处理中..."
        else:
            desired = "idle"
            detail = "等待任务中..."

        if last_state != desired or state.get("detail") != detail:
            state["state"] = desired
            state["detail"] = detail
            state["updated_at"] = datetime.now().isoformat()
            save_state(state)
            last_state = desired

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
