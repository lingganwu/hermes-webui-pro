"""
Hermes WebUI Pro - FastAPI 后端
"""
import os
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import jwt
import json

from hermes_client import (
    get_health, get_gateway_status, get_model_config, get_providers,
    get_cron_jobs, get_skills, get_memories, get_memory_content,
    get_sessions, get_config, update_config, get_logs, get_log_content,
    get_usage, get_state_db_stats, get_workflows, get_all_models,
    read_yaml_config
)

app = FastAPI(title="Hermes WebUI Pro", version="2.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 配置
JWT_SECRET = os.getenv("JWT_SECRET", "hermes-webui-pro-secret-key-2024")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 72
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "hermes2024")


class LoginRequest(BaseModel):
    password: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ConfigUpdateRequest(BaseModel):
    updates: dict


def create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    return jwt.encode({**data, "exp": expire}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(authorization: str = Depends(lambda: None)):
    # 简化认证，从 header 获取 token
    pass


# ==================== 认证 ====================

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    if req.password != LOGIN_PASSWORD:
        raise HTTPException(status_code=401, detail="密码错误")
    token = create_token({"user": "admin"})
    return {"token": token, "user": "admin"}


@app.get("/api/auth/verify")
async def verify_auth(token: str):
    payload = verify_token(token)
    return {"valid": True, "user": payload.get("user")}


# ==================== Dashboard ====================

@app.get("/api/dashboard")
async def get_dashboard(token: str):
    verify_token(token)
    return {
        "health": get_health(),
        "gateway": get_gateway_status(),
        "models": get_model_config(),
        "jobs": get_cron_jobs(),
        "skills_count": len(get_skills()),
        "sessions_count": len(get_sessions()),
        "memories_count": len(get_memories()),
    }


# ==================== 健康状态 ====================

@app.get("/api/health")
async def health(token: str):
    verify_token(token)
    return get_health()


# ==================== 网关状态 ====================

@app.get("/api/gateways")
async def gateways(token: str):
    verify_token(token)
    return get_gateway_status()


# ==================== 模型 ====================

@app.get("/api/models")
async def models(token: str):
    verify_token(token)
    return get_all_models()


@app.get("/api/models/config")
async def models_config(token: str):
    verify_token(token)
    return get_model_config()


@app.get("/api/providers")
async def providers(token: str):
    verify_token(token)
    return get_providers()


# ==================== 定时任务 ====================

@app.get("/api/jobs")
async def jobs(token: str):
    verify_token(token)
    return {"jobs": get_cron_jobs()}


# ==================== 技能 ====================

@app.get("/api/skills")
async def skills(token: str):
    verify_token(token)
    return {"skills": get_skills()}


# ==================== 记忆 ====================

@app.get("/api/memory")
async def memory(token: str):
    verify_token(token)
    return {"memories": get_memories()}


@app.get("/api/memory/{name}")
async def memory_content(name: str, token: str):
    verify_token(token)
    content = get_memory_content(name)
    if not content:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"name": name, "content": content}


# ==================== 会话 ====================

@app.get("/api/sessions")
async def sessions(token: str, limit: int = 50):
    verify_token(token)
    return {"sessions": get_sessions(limit)}


# ==================== 配置 ====================

@app.get("/api/config")
async def config(token: str):
    verify_token(token)
    return get_config()


@app.put("/api/config")
async def update_config_api(req: ConfigUpdateRequest, token: str):
    verify_token(token)
    return update_config(req.updates)


# ==================== 日志 ====================

@app.get("/api/logs")
async def logs(token: str):
    verify_token(token)
    return {"logs": get_logs()}


@app.get("/api/logs/{name}")
async def log_content(name: str, token: str, lines: int = 100):
    verify_token(token)
    content = get_log_content(name, lines)
    return {"name": name, "content": content}


# ==================== 使用统计 ====================

@app.get("/api/usage")
async def usage(token: str):
    verify_token(token)
    return get_usage()


# ==================== 工作流 ====================

@app.get("/api/workflows")
async def workflows(token: str):
    verify_token(token)
    return {"workflows": get_workflows()}


# ==================== 聊天 ====================

@app.post("/api/chat")
async def chat(req: ChatRequest, token: str):
    verify_token(token)
    # 聊天功能通过 WebSocket 实现，这里返回提示
    return {"message": "请使用 WebSocket 连接进行实时聊天", "ws_url": "/ws/chat"}


# ==================== WebSocket 聊天 ====================

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            # 简单回显，实际应该调用 Hermes Agent
            response = {
                "type": "message",
                "content": f"收到消息: {msg.get('message', '')}",
                "timestamp": datetime.now().isoformat(),
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass


# ==================== 静态文件 ====================

# 挂载前端静态文件
static_dir = "/app/static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # 所有非 API 路径返回 index.html
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
