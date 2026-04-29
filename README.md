# 🔮 Hermes WebUI Pro

**A stunning, production-ready web interface for Hermes AI Agent by Nous Research.**

Hermes WebUI Pro provides a sleek, modern dashboard for interacting with your Hermes AI agent. Monitor system performance, chat in real-time, explore models and skills, all from a beautiful dark-themed interface.

---

## ✨ Features

- 📊 **Dashboard** — Real-time system metrics: CPU, memory, disk, uptime, and gateway status
- 💬 **Chat** — Direct conversation with Hermes AI with session management and history
- 🔮 **SoulTrace** — Create your AI soulmate through guided personality questions
- 🤖 **Models** — Browse available AI models with tier distribution (fast, balanced, quality)
- 🛠️ **Skills** — View and manage installed Hermes agent skills
- ⚙️ **Settings** — Configure environment variables, preferences, and system settings

---

## 📸 Screenshots

> Coming soon — screenshots of the dashboard, chat interface, and SoulTrace wizard.

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/hermes-webui-pro.git
cd hermes-webui-pro

# Start with Docker Compose
docker-compose up -d --build

# Open in browser
open http://localhost:8765
```

### Manual Setup

```bash
# Prerequisites: Python 3.10+, Hermes CLI installed

# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py

# Or with uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 8765 --reload
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HERMES_HOME` | `~/.hermes` | Path to Hermes config directory |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `METRICS_INTERVAL` | `10` | System metrics collection interval (seconds) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check with uptime |
| `GET` | `/api/metrics` | System and gateway metrics |
| `POST` | `/api/chat` | Send message to Hermes agent |
| `GET` | `/api/sessions` | List chat sessions |
| `POST` | `/api/soultrace` | Proxy to SoulTrace API |
| `GET` | `/api/models` | List available AI models |
| `GET` | `/api/skills` | List installed skills |
| `GET` | `/api/cron` | List scheduled cron jobs |
| `WS` | `/ws` | WebSocket for real-time chat |

### Chat Request Example

```bash
curl -X POST http://localhost:8765/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Hermes!", "session_id": "my-session"}'
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser Client                        │
│              (HTML/CSS/JavaScript SPA)                   │
└──────────────┬──────────────────────────┬───────────────┘
               │  HTTP REST              │  WebSocket
               ▼                          ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Server (port 8765)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ REST API │ │WebSocket │ │Static    │ │Background │  │
│  │Endpoints │ │ Handler  │ │Files     │ │ Metrics   │  │
│  └────┬─────┘ └────┬─────┘ └──────────┘ └─────┬─────┘  │
└───────┼─────────────┼──────────────────────────┼────────┘
        │             │                          │
        ▼             ▼                          ▼
┌──────────────┐ ┌──────────┐           ┌───────────────┐
│ Hermes CLI   │ │SoulTrace │           │    psutil     │
│ (subprocess) │ │   API    │           │(system stats) │
└──────────────┘ └──────────┘           └───────────────┘
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-4CAF50?logo=uvicorn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

Built with ❤️ for **Hermes Agent** by [Nous Research](https://nousresearch.com).

Hermes Agent is an intelligent AI assistant framework — learn more at [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com).
