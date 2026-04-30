import os
import json
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from auth import verify_password, create_token, verify_token
from hermes_bridge import (
    chat_send, get_memory_entries, write_memory_content,
    get_skills_list, get_config, get_sessions_list, get_session_messages,
    get_hermes_home,
)
import psutil

# ── Auth dependency ──
async def require_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing token")
    token = auth[7:]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    return payload

# ── App ──
app = FastAPI(title="Hermes WebUI Pro", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth routes ──
@app.post("/api/auth/login")
async def login(request: Request):
    body = await request.json()
    password = body.get("password", "")
    if not verify_password(password):
        raise HTTPException(401, "密码错误")
    token = create_token({"sub": "hermes-webui"})
    return {"token": token, "expires_in": 86400}

@app.get("/api/auth/verify")
async def verify_auth(payload=Depends(require_auth)):
    return {"valid": True, "user": payload.get("sub")}

# ── Health / System ──
@app.get("/api/health")
async def health():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "status": "ok",
        "cpu": round(cpu, 1),
        "memory": round(mem.percent, 1),
        "disk": round(disk.percent, 1),
        "uptime": _format_uptime(),
        "hermes_home": str(get_hermes_home()),
    }

@app.get("/api/metrics")
async def metrics():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {"cpu": round(cpu, 1), "memory": round(mem.percent, 1), "disk": round(disk.percent, 1)}

def _format_uptime() -> str:
    import time
    uptime_s = time.time() - psutil.boot_time()
    d = int(uptime_s // 86400)
    h = int((uptime_s % 86400) // 3600)
    m = int((uptime_s % 3600) // 60)
    parts = []
    if d: parts.append(f"{d}d")
    if h: parts.append(f"{h}h")
    parts.append(f"{m}m")
    return " ".join(parts)

# ── Chat ──
@app.get("/api/sessions")
async def list_sessions(payload=Depends(require_auth)):
    return {"sessions": get_sessions_list()}

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str, payload=Depends(require_auth)):
    return {"messages": get_session_messages(session_id)}

@app.post("/api/chat")
async def chat(request: Request, payload=Depends(require_auth)):
    body = await request.json()
    message = body.get("message", "")
    model = body.get("model")
    if not message:
        raise HTTPException(400, "Message required")
    response = await chat_send(message, model)
    return {"response": response}

# ── Memory ──
@app.get("/api/memory")
async def memory_list(payload=Depends(require_auth)):
    return {"entries": get_memory_entries()}

@app.put("/api/memory/{entry_id}")
async def memory_update(entry_id: str, request: Request, payload=Depends(require_auth)):
    body = await request.json()
    content = body.get("content", "")
    write_memory_content(content)
    return {"success": True}

@app.post("/api/memory")
async def memory_create(request: Request, payload=Depends(require_auth)):
    body = await request.json()
    content = body.get("content", "")
    # Append to SOUL.md
    soul_path = get_hermes_home() / "SOUL.md"
    existing = soul_path.read_text(encoding="utf-8") if soul_path.exists() else ""
    new_content = existing + "\n\n" + content
    write_memory_content(new_content)
    return {"success": True}

# ── Jobs ──
@app.get("/api/jobs")
async def list_jobs(payload=Depends(require_auth)):
    jobs = []
    return {"jobs": jobs}

@app.post("/api/jobs/{job_id}/run")
async def run_job(job_id: str, payload=Depends(require_auth)):
    return {"success": True, "output": "Job triggered"}

@app.post("/api/jobs/{job_id}/toggle")
async def toggle_job(job_id: str, request: Request, payload=Depends(require_auth)):
    body = await request.json()
    action = "resume" if body.get("enabled") else "pause"
    return {"success": True}

# ── Models ──
@app.get("/api/models")
async def list_models(payload=Depends(require_auth)):
    config = get_config()
    model_info = config.get("model", {})
    models = [{"id": model_info.get("default", "unknown"), "name": model_info.get("default", "unknown"), "provider": model_info.get("provider", ""), "tier": "active"}]
    return {"models": models}

# ── Skills ──
@app.get("/api/skills")
async def list_skills(payload=Depends(require_auth)):
    return {"skills": get_skills_list()}

# ── Config ──
@app.get("/api/config")
async def config_get(payload=Depends(require_auth)):
    return get_config()

@app.put("/api/config")
async def config_update(request: Request, payload=Depends(require_auth)):
    import yaml
    body = await request.json()
    config_path = get_hermes_home() / "config.yaml"
    current = get_config()
    current.update(body)
    config_path.write_text(yaml.dump(current, allow_unicode=True), encoding="utf-8")
    return {"success": True}

# ── Logs ──
@app.get("/api/logs")
async def get_logs(payload=Depends(require_auth)):
    log_path = get_hermes_home() / "logs" / "gateway.log"
    lines = []
    if log_path.exists():
        try:
            all_lines = log_path.read_text(encoding="utf-8").split("\n")
            lines = all_lines[-500:]  # Last 500 lines
        except: pass
    return {"lines": lines}

# ── Usage ──
@app.get("/api/usage")
async def get_usage(payload=Depends(require_auth)):
    # Aggregate from session files
    sessions = get_sessions_list()
    total_input = sum(s.get("inputTokens", 0) for s in sessions)
    total_output = sum(s.get("outputTokens", 0) for s in sessions)
    return {
        "totalCalls": len(sessions),
        "totalInputTokens": total_input,
        "totalOutputTokens": total_output,
        "estimatedCost": f"{(total_input * 0.000003 + total_output * 0.000015):.2f}",
        "modelBreakdown": [],
    }

# ── Gateways ──
@app.get("/api/gateways")
async def list_gateways(payload=Depends(require_auth)):
    gateways = [{"name": "telegram", "connected": True, "platform": "telegram"}]
    return {"gateways": gateways}

# ── WebSocket: Chat streaming ──
@app.websocket("/ws/chat")
async def ws_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            message = msg.get("message", "")
            model = msg.get("model")
            if message:
                response = await chat_send(message, model)
                await websocket.send_text(json.dumps({"type": "response", "content": response}))
    except WebSocketDisconnect:
        pass

# ── WebSocket: Terminal ──
@app.websocket("/ws/terminal")
async def ws_terminal(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            command = msg.get("command", "")
            if command:
                proc = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
                output = stdout.decode("utf-8", errors="replace")
                if stderr:
                    output += stderr.decode("utf-8", errors="replace")
                await websocket.send_text(output)
    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        await websocket.send_text("Command timed out")

# ── Serve static files (production) ──
client_dist = Path(__file__).parent.parent / "client" / "dist"
if client_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(client_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = client_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(client_dist / "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
