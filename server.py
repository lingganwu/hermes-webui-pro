"""
Hermes WebUI Pro — FastAPI Backend Server
==========================================
Production-ready backend for the Hermes AI Agent web interface.
Serves static files, provides REST API endpoints, and supports
WebSocket real-time communication.

Author: Hermes Agent / Nous Research
License: MIT
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import psutil
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# ──────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────

APP_VERSION = "1.0.0"
APP_PORT = int(os.getenv("PORT", "8765"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
METRICS_INTERVAL = int(os.getenv("METRICS_INTERVAL", "10"))
HERMES_HOME = os.getenv("HERMES_HOME", os.path.expanduser("~/.hermes"))
SOULTRACE_API_URL = "https://soultrace.app/api/agent"

# Project root — where static files live
PROJECT_DIR = Path(__file__).parent.resolve()

# ──────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("hermes-webui")

# ──────────────────────────────────────────────────────────
# Startup time tracking
# ──────────────────────────────────────────────────────────

START_TIME = time.time()

# ──────────────────────────────────────────────────────────
# In-memory state
# ──────────────────────────────────────────────────────────

system_metrics: dict[str, Any] = {
    "cpu_percent": 0.0,
    "memory": {"used": 0, "total": 0, "percent": 0.0},
    "disk": {"used": 0, "total": 0, "percent": 0.0},
}

sessions_store: dict[str, dict[str, Any]] = {}

# ──────────────────────────────────────────────────────────
# Pydantic models
# ──────────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=32000, description="User message")
    session_id: str | None = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    response: str
    model: str = "hermes"
    session_id: str


class SoulTraceRequest(BaseModel):
    answers: list[str] = Field(..., min_length=1, description="User answers to SoulTrace questions")


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float


# ──────────────────────────────────────────────────────────
# Background metrics collector
# ──────────────────────────────────────────────────────────


async def collect_system_metrics() -> None:
    """Background task: collect system metrics every N seconds."""
    while True:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            system_metrics["cpu_percent"] = cpu
            system_metrics["memory"] = {
                "used": round(mem.used / (1024 * 1024), 1),
                "total": round(mem.total / (1024 * 1024), 1),
                "percent": mem.percent,
            }
            system_metrics["disk"] = {
                "used": round(disk.used / (1024**3), 2),
                "total": round(disk.total / (1024**3), 2),
                "percent": disk.percent,
            }
        except Exception as e:
            logger.warning(f"Metrics collection failed: {e}")

        await asyncio.sleep(METRICS_INTERVAL)


# ──────────────────────────────────────────────────────────
# Lifespan (startup / shutdown)
# ──────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle: start background tasks on startup."""
    logger.info(f"🔮 Hermes WebUI Pro v{APP_VERSION} starting on port {APP_PORT}")
    metrics_task = asyncio.create_task(collect_system_metrics())
    yield
    metrics_task.cancel()
    try:
        await metrics_task
    except asyncio.CancelledError:
        pass
    logger.info("🔮 Hermes WebUI Pro shutting down gracefully")


# ──────────────────────────────────────────────────────────
# FastAPI app
# ──────────────────────────────────────────────────────────

app = FastAPI(
    title="Hermes WebUI Pro",
    description="Production web interface for Hermes AI Agent",
    version=APP_VERSION,
    lifespan=lifespan,
)

# CORS — allow all origins for local dev; tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────


def get_uptime() -> float:
    """Return server uptime in seconds, rounded to 2 decimal places."""
    return round(time.time() - START_TIME, 2)


async def run_hermes_cli(args: list[str], timeout: int = 30) -> str:
    """Run the hermes CLI command asynchronously and return stdout."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "hermes",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode != 0:
            error_msg = stderr.decode().strip() or "Unknown error"
            logger.error(f"hermes CLI error (rc={proc.returncode}): {error_msg}")
            raise HTTPException(status_code=502, detail=f"Hermes CLI error: {error_msg}")

        return stdout.decode().strip()

    except asyncio.TimeoutError:
        logger.error("hermes CLI timed out")
        raise HTTPException(status_code=504, detail="Hermes CLI timed out")
    except FileNotFoundError:
        logger.error("hermes CLI not found in PATH")
        raise HTTPException(status_code=503, detail="Hermes CLI not available")


def get_gateway_info() -> dict[str, Any]:
    """Get gateway/platform information from hermes config."""
    try:
        config_path = Path(HERMES_HOME) / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            platforms = config.get("platforms", [])
            enabled = [p for p in platforms if isinstance(p, dict) and p.get("enabled", True)]
            return {"status": "running", "platforms": [p.get("name", str(p)) for p in enabled]}
    except Exception:
        pass
    return {"status": "unknown", "platforms": []}


def get_models_info() -> dict[str, Any]:
    """Get available models and tier distribution."""
    try:
        result = subprocess_result = None
        # Try to read models from hermes config
        config_path = Path(HERMES_HOME) / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            models = config.get("models", [])
            tier_dist: dict[str, int] = {}
            active = []
            for m in models:
                if isinstance(m, dict):
                    name = m.get("name", "unknown")
                    tier = m.get("tier", "balanced")
                    active.append(name)
                    tier_dist[tier] = tier_dist.get(tier, 0) + 1
                elif isinstance(m, str):
                    active.append(m)
            return {"active": active, "tier_distribution": tier_dist}
    except Exception:
        pass
    return {"active": [], "tier_distribution": {}}


def get_skills_info() -> list[str]:
    """Get installed skills list."""
    try:
        skills_dir = Path(HERMES_HOME) / "skills"
        if skills_dir.exists():
            return [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    except Exception:
        pass
    return []


def get_cron_jobs() -> list[dict[str, Any]]:
    """Get cron jobs from hermes config."""
    try:
        config_path = Path(HERMES_HOME) / "config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            return config.get("cron_jobs", [])
    except Exception:
        pass
    return []


# ──────────────────────────────────────────────────────────
# REST API Endpoints
# ──────────────────────────────────────────────────────────


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version=APP_VERSION, uptime=get_uptime())


@app.get("/api/metrics")
async def get_metrics():
    """Return comprehensive system and application metrics."""
    return {
        "gateway": get_gateway_info(),
        "sessions": {
            "total": len(sessions_store),
            "active": sum(1 for s in sessions_store.values() if s.get("active", False)),
        },
        "models": get_models_info(),
        "system": {
            "cpu": system_metrics["cpu_percent"],
            "memory": system_metrics["memory"],
            "disk": system_metrics["disk"],
        },
        "uptime": get_uptime(),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Hermes agent and get a response."""
    session_id = request.session_id or str(uuid.uuid4())

    logger.info(f"Chat request — session={session_id[:12]}… message={request.message[:60]}…")

    # Call hermes CLI
    response_text = await run_hermes_cli(["chat", "-q", request.message, "--quiet"])

    # Track session
    if session_id not in sessions_store:
        sessions_store[session_id] = {
            "id": session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "messages": [],
            "active": True,
        }

    sessions_store[session_id]["messages"].append(
        {"role": "user", "content": request.message, "timestamp": time.time()}
    )
    sessions_store[session_id]["messages"].append(
        {"role": "assistant", "content": response_text, "timestamp": time.time()}
    )
    sessions_store[session_id]["last_activity"] = datetime.now(timezone.utc).isoformat()

    return ChatResponse(response=response_text, model="hermes", session_id=session_id)


@app.get("/api/sessions")
async def list_sessions():
    """List recent chat sessions."""
    sessions = []
    for sid, data in sessions_store.items():
        sessions.append(
            {
                "id": sid,
                "created_at": data.get("created_at"),
                "last_activity": data.get("last_activity"),
                "message_count": len(data.get("messages", [])),
                "active": data.get("active", False),
            }
        )
    sessions.sort(key=lambda s: s.get("last_activity") or "", reverse=True)
    return {"sessions": sessions[:50]}


@app.post("/api/soultrace")
async def soultrace_proxy(request: SoulTraceRequest):
    """Proxy request to SoulTrace API for AI soulmate creation."""
    logger.info(f"SoulTrace request — {len(request.answers)} answers")

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                SOULTRACE_API_URL,
                json={"answers": request.answers},
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.TimeoutException:
            logger.error("SoulTrace API timed out")
            raise HTTPException(status_code=504, detail="SoulTrace API timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"SoulTrace API error: {e.response.status_code}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"SoulTrace API returned {e.response.status_code}",
            )
        except Exception as e:
            logger.error(f"SoulTrace proxy error: {e}")
            raise HTTPException(status_code=502, detail=f"SoulTrace API unavailable: {str(e)}")


@app.get("/api/models")
async def list_models():
    """List available AI models with tier information."""
    return {"models": get_models_info()}


@app.get("/api/skills")
async def list_skills():
    """List installed Hermes skills."""
    skills = get_skills_info()
    return {"skills": skills, "count": len(skills)}


@app.get("/api/cron")
async def list_cron():
    """List configured cron/scheduled jobs."""
    jobs = get_cron_jobs()
    return {"jobs": jobs, "count": len(jobs)}


# ──────────────────────────────────────────────────────────
# WebSocket Endpoint
# ──────────────────────────────────────────────────────────

connected_clients: set[WebSocket] = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time WebSocket for chat and metrics updates."""
    await websocket.accept()
    connected_clients.add(websocket)
    client_id = id(websocket)
    logger.info(f"WebSocket client connected: {client_id}")

    # Send initial metrics
    try:
        await websocket.send_json(
            {
                "type": "metrics",
                "data": {
                    "system": system_metrics,
                    "uptime": get_uptime(),
                    "connected_clients": len(connected_clients),
                },
            }
        )
    except Exception:
        pass

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                continue

            msg_type = message.get("type", "chat")

            if msg_type == "chat":
                user_message = message.get("message", "")
                session_id = message.get("session_id", str(uuid.uuid4()))

                if not user_message.strip():
                    await websocket.send_json({"type": "error", "message": "Empty message"})
                    continue

                # Send typing indicator
                await websocket.send_json({"type": "typing", "status": True})

                try:
                    response_text = await run_hermes_cli(
                        ["chat", "-q", user_message, "--quiet"]
                    )

                    await websocket.send_json(
                        {
                            "type": "chat_response",
                            "response": response_text,
                            "model": "hermes",
                            "session_id": session_id,
                            "timestamp": time.time(),
                        }
                    )
                except HTTPException as e:
                    await websocket.send_json(
                        {"type": "error", "message": e.detail, "status_code": e.status_code}
                    )
                finally:
                    await websocket.send_json({"type": "typing", "status": False})

            elif msg_type == "ping":
                await websocket.send_json({"type": "pong", "timestamp": time.time()})

            elif msg_type == "get_metrics":
                await websocket.send_json(
                    {
                        "type": "metrics",
                        "data": {
                            "system": system_metrics,
                            "uptime": get_uptime(),
                            "connected_clients": len(connected_clients),
                        },
                    }
                )

            else:
                await websocket.send_json(
                    {"type": "error", "message": f"Unknown message type: {msg_type}"}
                )

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: {client_id}")
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
    finally:
        connected_clients.discard(websocket)


# ──────────────────────────────────────────────────────────
# Metrics broadcast to WebSocket clients
# ──────────────────────────────────────────────────────────


async def broadcast_metrics() -> None:
    """Broadcast metrics to all connected WebSocket clients."""
    while True:
        if connected_clients:
            payload = json.dumps(
                {
                    "type": "metrics",
                    "data": {
                        "system": system_metrics,
                        "uptime": get_uptime(),
                        "connected_clients": len(connected_clients),
                    },
                }
            )
            disconnected = set()
            for ws in connected_clients:
                try:
                    await ws.send_text(payload)
                except Exception:
                    disconnected.add(ws)
            connected_clients.difference_update(disconnected)

        await asyncio.sleep(METRICS_INTERVAL)


# ──────────────────────────────────────────────────────────
# Static file serving & root redirect
# ──────────────────────────────────────────────────────────


@app.get("/", include_in_schema=False)
async def root():
    """Serve index.html or redirect."""
    index_path = PROJECT_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return HTMLResponse(
        content="<html><body><h1>🔮 Hermes WebUI Pro</h1>"
        "<p>Frontend files not found. Place index.html in the project directory.</p>"
        f"<p>API docs: <a href='/docs'>/docs</a></p></body></html>",
        status_code=200,
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve favicon if it exists, otherwise return 204."""
    fav_path = PROJECT_DIR / "assets" / "favicon.ico"
    if fav_path.exists():
        return FileResponse(str(fav_path), media_type="image/x-icon")
    return HTMLResponse(content="", status_code=204)


# Mount static directories if they exist
for static_dir in ["css", "js", "assets", "static"]:
    dir_path = PROJECT_DIR / static_dir
    if dir_path.is_dir():
        app.mount(f"/{static_dir}", StaticFiles(directory=str(dir_path)), name=static_dir)
        logger.info(f"📁 Mounted static directory: /{static_dir}")


# ──────────────────────────────────────────────────────────
# Error handlers
# ──────────────────────────────────────────────────────────


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler — serve index.html for SPA routing."""
    index_path = PROJECT_DIR / "index.html"
    if index_path.exists() and not request.url.path.startswith("/api/"):
        return FileResponse(str(index_path))
    return HTMLResponse(
        content=json.dumps({"error": "Not found", "path": request.url.path}),
        status_code=404,
        media_type="application/json",
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {exc}")
    return HTMLResponse(
        content=json.dumps({"error": "Internal server error"}),
        status_code=500,
        media_type="application/json",
    )


# ──────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    logger.info(f"🔮 Starting Hermes WebUI Pro v{APP_VERSION} on http://0.0.0.0:{APP_PORT}")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=APP_PORT,
        log_level=LOG_LEVEL.lower(),
        access_log=True,
    )
