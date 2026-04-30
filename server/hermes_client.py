"""
Hermes 数据客户端 - 直接读取文件系统
"""
import os
import json
import yaml
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

HERMES_DATA = Path(os.getenv("HERMES_DATA_PATH", "/hermes-data"))


def read_yaml_config() -> dict:
    """读取 config.yaml"""
    cfg_path = HERMES_DATA / "config.yaml"
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def write_yaml_config(data: dict):
    """写入 config.yaml"""
    cfg_path = HERMES_DATA / "config.yaml"
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def read_json(path: Path) -> Any:
    """读取 JSON 文件"""
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_health() -> dict:
    """获取系统健康状态"""
    import psutil
    disk = psutil.disk_usage("/")
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "percent": disk.percent,
        },
        "hermes_data": str(HERMES_DATA),
        "hermes_exists": HERMES_DATA.exists(),
    }


def get_gateway_status() -> dict:
    """获取网关状态"""
    state = read_json(HERMES_DATA / "gateway_state.json")
    if state:
        return {
            "state": state.get("gateway_state", "unknown"),
            "pid": state.get("pid"),
            "start_time": state.get("start_time"),
            "platforms": state.get("platforms", {}),
            "updated_at": state.get("updated_at"),
            "active_agents": state.get("active_agents", 0),
        }
    return {"state": "not_found", "platforms": {}}


def get_model_config() -> dict:
    """获取模型配置"""
    cfg = read_yaml_config()
    model = cfg.get("model", {})
    providers = cfg.get("providers", {})
    fallback = cfg.get("fallback_providers", [])
    
    # 读取 free_models.json 获取可用模型列表
    free_models = read_json(HERMES_DATA / "free_models.json") or {}
    
    return {
        "default_model": model.get("default", "unknown"),
        "default_provider": model.get("provider", "unknown"),
        "base_url": model.get("base_url", ""),
        "providers": providers,
        "fallback_providers": fallback,
        "free_models_count": len(free_models.get("models", [])) if isinstance(free_models, dict) else 0,
    }


def get_providers() -> List[dict]:
    """获取所有 Provider"""
    cfg = read_yaml_config()
    providers = cfg.get("providers", {})
    fallback = cfg.get("fallback_providers", [])
    
    result = []
    # 主 provider
    model = cfg.get("model", {})
    if model.get("provider"):
        result.append({
            "name": model["provider"],
            "type": "primary",
            "model": model.get("default", ""),
            "base_url": model.get("base_url", ""),
        })
    
    # fallback providers
    for fb in fallback:
        result.append({
            "name": fb.get("provider", "unknown"),
            "type": "fallback",
            "model": fb.get("model", ""),
            "base_url": fb.get("base_url", ""),
        })
    
    return result


def get_cron_jobs() -> List[dict]:
    """获取定时任务"""
    jobs_data = read_json(HERMES_DATA / "cron" / "jobs.json")
    if jobs_data and "jobs" in jobs_data:
        return jobs_data["jobs"]
    return []


def get_skills() -> List[dict]:
    """获取技能列表"""
    skills_dir = HERMES_DATA / "skills"
    cfg = read_yaml_config()
    disabled = cfg.get("skills", {}).get("disabled", [])
    
    result = []
    if skills_dir.exists():
        for cat_dir in sorted(skills_dir.iterdir()):
            if not cat_dir.is_dir() or cat_dir.name.startswith("."):
                continue
            for skill_dir in sorted(cat_dir.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text(encoding="utf-8", errors="ignore")
                    # 提取描述
                    desc = ""
                    for line in content.split("\n"):
                        if line.strip() and not line.startswith("#") and not line.startswith("---"):
                            desc = line.strip()[:100]
                            break
                    result.append({
                        "name": skill_dir.name,
                        "category": cat_dir.name,
                        "description": desc,
                        "enabled": skill_dir.name not in disabled,
                    })
    return result


def get_memories() -> List[dict]:
    """获取记忆列表"""
    mem_dir = HERMES_DATA / "memories"
    result = []
    if mem_dir.exists():
        for f in sorted(mem_dir.iterdir()):
            if f.is_file() and not f.name.endswith(".lock"):
                content = f.read_text(encoding="utf-8", errors="ignore")
                result.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    "preview": content[:200] if content else "",
                })
    return result


def get_memory_content(name: str) -> str:
    """获取记忆内容"""
    mem_file = HERMES_DATA / "memories" / name
    if mem_file.exists():
        return mem_file.read_text(encoding="utf-8", errors="ignore")
    return ""


def get_sessions(limit: int = 50) -> List[dict]:
    """获取会话列表"""
    sessions_dir = HERMES_DATA / "sessions"
    result = []
    if sessions_dir.exists():
        sessions = sorted(sessions_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        for s in sessions[:limit]:
            if s.is_dir():
                meta_file = s / "meta.json"
                if meta_file.exists():
                    meta = read_json(meta_file) or {}
                    result.append({
                        "id": s.name,
                        "title": meta.get("title", s.name),
                        "created_at": meta.get("created_at", ""),
                        "updated_at": meta.get("updated_at", ""),
                        "message_count": meta.get("message_count", 0),
                    })
                else:
                    result.append({
                        "id": s.name,
                        "title": s.name,
                        "created_at": "",
                        "updated_at": "",
                        "message_count": 0,
                    })
    return result


def get_config() -> dict:
    """获取完整配置"""
    cfg = read_yaml_config()
    return {
        "model": cfg.get("model", {}),
        "providers": cfg.get("providers", {}),
        "fallback_providers": cfg.get("fallback_providers", []),
        "agent": cfg.get("agent", {}),
        "terminal": cfg.get("terminal", {}),
        "browser": cfg.get("browser", {}),
        "checkpoints": cfg.get("checkpoints", {}),
        "compression": cfg.get("compression", {}),
        "prompt_caching": cfg.get("prompt_caching", {}),
        "toolsets": cfg.get("toolsets", []),
    }


def update_config(updates: dict) -> dict:
    """更新配置"""
    cfg = read_yaml_config()
    cfg.update(updates)
    write_yaml_config(cfg)
    return cfg


def get_logs(limit: int = 100) -> List[dict]:
    """获取日志列表"""
    logs_dir = HERMES_DATA / "logs"
    result = []
    if logs_dir.exists():
        for f in sorted(logs_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)[:limit]:
            if f.is_file():
                result.append({
                    "name": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                })
    return result


def get_log_content(name: str, lines: int = 100) -> str:
    """获取日志内容"""
    log_file = HERMES_DATA / "logs" / name
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8", errors="ignore")
        return "\n".join(content.split("\n")[-lines:])
    return ""


def get_usage() -> dict:
    """获取使用统计"""
    usage_file = HERMES_DATA / "model_usage.json"
    usage = read_json(usage_file) or {}
    return usage


def get_state_db_stats() -> dict:
    """从 state.db 获取统计信息"""
    db_path = HERMES_DATA / "state.db"
    if not db_path.exists():
        return {}
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 获取表列表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        stats = {"tables": tables}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                stats[f"{table}_count"] = cursor.fetchone()[0]
            except:
                pass
        
        conn.close()
        return stats
    except Exception as e:
        return {"error": str(e)}


def get_workflows() -> list:
    """获取工作流"""
    wf = read_json(HERMES_DATA / "workflows.json")
    return wf if isinstance(wf, list) else []


def get_all_models() -> List[dict]:
    """获取所有可用模型"""
    free_models = read_json(HERMES_DATA / "free_models.json") or {}
    models = free_models.get("models", []) if isinstance(free_models, dict) else []
    
    # 添加当前配置的模型
    cfg = read_yaml_config()
    current = cfg.get("model", {})
    
    return {
        "current": current,
        "free_models": models[:50],  # 限制返回数量
        "total_free": len(models),
    }
