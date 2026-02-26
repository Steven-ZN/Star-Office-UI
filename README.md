# Star Office UI

[中文说明](README_CN.md)

A tiny “pixel office” status UI for your AI assistant.

- Pixel office background (top-down, customizable). **This repo includes a sample background (office_bg.png).**
- Avatar switches animations (walking/rushing/alert) based on `state`.
- Optional speech bubble / typing effect.
- **Optional Gateway logs + TUI status side panels (built-in).**
- Mobile-friendly access via Cloudflare Tunnel quick tunnel.

> Language: English is the default. Chinese doc is in README_CN.md.

## What it looks like

![UI Preview](frontend/office_bg.png)

**Added in this fork:**
- Sample background image included
- Gateway logs + TUI status side panels
- Multiple avatar sprites + motion rules (walking/rushing/alert)

- `idle / syncing` → breakroom area
- `writing / researching` → desk area
- `executing` → execution area
- `error` → alert area

The UI polls `/status` and renders the assistant avatar accordingly.

## Folder structure

```
star-office-ui/
  backend/        # Flask backend (serves index + status)
  frontend/       # Phaser frontend + office_bg.png
  state.json      # runtime status file
  set_state.py    # helper to update state.json
```

## Requirements

- Python 3.9+
- Flask

## Quick start (local)

### 1) Install dependencies

```bash
pip install flask
```

### 2) Put your background image

Put a **800×600 PNG** at:

```
star-office-ui/frontend/office_bg.png
```

### 3) Start backend

```bash
cd star-office-ui/backend
python app.py
```

Then open:

- http://127.0.0.1:18791

### 4) Update status

From the project root:

```bash
python3 star-office-ui/set_state.py writing "Working on a task..."
python3 star-office-ui/set_state.py idle "Standing by"
```

## Public access (Cloudflare quick tunnel)

Install `cloudflared`, then:

```bash
cloudflared tunnel --url http://127.0.0.1:18791
```

You’ll get a `https://xxx.trycloudflare.com` URL.

## Security notes

- quick tunnel URL may change, no uptime guarantee
- `/status` is public; don’t put secrets in detail
- For privacy: add token / hide detail
