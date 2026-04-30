# ⚡ Hermes WebUI Pro

> Vue 3 + Naive UI + FastAPI — Professional Web Dashboard for Hermes Agent

A modern, feature-rich web interface for [Hermes Agent](https://github.com/nousresearch/hermes-agent) with JWT authentication, dark/light themes, and comprehensive management capabilities.

## ✨ Features

- 🔐 **JWT Password Login** — Secure external access
- 💬 **AI Chat** — Real-time conversation with Hermes
- 🧠 **Memory Management** — CRUD Hermes memory entries
- ⏰ **Job Scheduler** — Manage cron jobs
- 🤖 **Model Manager** — View and select AI models
- 🛠 **Skills Browser** — Browse installed skills
- 💻 **Terminal** — Web-based shell access
- 📊 **Usage Analytics** — Token usage and cost tracking
- 📋 **Log Viewer** — Real-time log monitoring
- 🌐 **Gateway Status** — Platform connection monitoring
- ⚙️ **Settings** — Configuration management
- 🌙 **Dark/Light Theme** — Toggle with smooth transitions
- 📱 **Responsive** — Works on desktop and mobile

## 🏗 Architecture

```
┌─────────────────────────────────────────┐
│           Vue 3 + Naive UI              │
│   (TypeScript, SCSS, Pinia, Vue Router) │
├─────────────────────────────────────────┤
│          FastAPI + JWT Auth             │
│    (WebSocket, REST API, CLI Bridge)    │
├─────────────────────────────────────────┤
│           Hermes Agent CLI              │
│    (Memory, Skills, Sessions, Cron)     │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Clone the repo
git clone https://github.com/lingganwu/hermes-webui-pro.git
cd hermes-webui-pro

# Configure
cp .env.example .env
# Edit .env to set your password

# Build and run
docker-compose up -d --build
```

Visit `http://your-server:8080` and login with your password.

### Manual Setup

```bash
# Frontend
cd client
npm install
npm run build

# Backend
cd ../server
pip install -r requirements.txt

# Set password
export HERMES_WEB_PASSWORD=your-password

# Run
python main.py
```

## 🔧 Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `HERMES_WEB_PASSWORD` | `hermes` | Access password |
| `HERMES_JWT_SECRET` | (auto) | JWT signing key |
| `HERMES_HOME` | `~/.hermes` | Hermes data directory |
| `PORT` | `8080` | Server port |

## 📁 Project Structure

```
hermes-webui-pro/
├── client/                 # Vue 3 frontend
│   ├── src/
│   │   ├── api/           # API layer (axios)
│   │   ├── components/    # Reusable components
│   │   ├── composables/   # Vue composables
│   │   ├── stores/        # Pinia state management
│   │   ├── styles/        # SCSS themes & variables
│   │   ├── views/         # Page components
│   │   └── router/        # Vue Router config
│   └── package.json
├── server/                 # FastAPI backend
│   ├── main.py            # App entry + routes
│   ├── auth.py            # JWT authentication
│   ├── hermes_bridge.py   # CLI bridge
│   └── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🛡 Security

- JWT tokens with 24h expiry
- Bcrypt password hashing
- All API routes protected (except login)
- WebSocket authentication via token query param

## 📄 License

MIT
