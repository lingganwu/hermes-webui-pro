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
    cfg_path = HERMES_DATA / "config.yaml"
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def write_yaml_config(data: dict):
    cfg_path = HERMES_DATA / "config.yaml"
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def read_json(path: Path) -> Any:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_health() -> dict:
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
        "hermes_exists": HERMES_DATA.exists(),
    }


def get_gateway_status() -> dict:
    state = read_json(HERMES_DATA / "gateway_state.json")
    if state:
        return {
            "state": state.get("gateway_state", "unknown"),
            "pid": state.get("pid"),
            "platforms": state.get("platforms", {}),
            "updated_at": state.get("updated_at"),
            "active_agents": state.get("active_agents", 0),
        }
    return {"state": "not_found", "platforms": {}}


def get_model_config() -> dict:
    cfg = read_yaml_config()
    model = cfg.get("model", {})
    fallback = cfg.get("fallback_providers", [])
    free_models = read_json(HERMES_DATA / "free_models.json") or {}
    
    return {
        "default_model": model.get("default", "unknown"),
        "default_provider": model.get("provider", "unknown"),
        "base_url": model.get("base_url", ""),
        "fallback_providers": fallback,
        "free_models_count": len(free_models.get("models", [])) if isinstance(free_models, dict) else 0,
    }


def get_providers() -> List[dict]:
    cfg = read_yaml_config()
    model = cfg.get("model", {})
    fallback = cfg.get("fallback_providers", [])
    
    result = []
    if model.get("provider"):
        result.append({
            "name": model["provider"],
            "type": "primary",
            "model": model.get("default", ""),
            "base_url": model.get("base_url", ""),
        })
    
    for fb in fallback:
        result.append({
            "name": fb.get("provider", "unknown"),
            "type": "fallback",
            "model": fb.get("model", ""),
            "base_url": fb.get("base_url", ""),
        })
    
    return result


def get_cron_jobs() -> List[dict]:
    jobs_data = read_json(HERMES_DATA / "cron" / "jobs.json")
    if jobs_data and "jobs" in jobs_data:
        return jobs_data["jobs"]
    return []


def get_skills() -> List[dict]:
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
    mem_file = HERMES_DATA / "memories" / name
    if mem_file.exists():
        return mem_file.read_text(encoding="utf-8", errors="ignore")
    return ""


def get_sessions(limit: int = 100) -> List[dict]:
    """获取会话列表 - 支持目录和 JSON 文件两种格式"""
    sessions_dir = HERMES_DATA / "sessions"
    result = []
    if not sessions_dir.exists():
        return result
    
    items = sorted(sessions_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
    count = 0
    
    for item in items:
        if count >= limit:
            break
        
        # 格式1: 目录格式 (有 meta.json)
        if item.is_dir():
            meta_file = item / "meta.json"
            if meta_file.exists():
                try:
                    meta = json.loads(meta_file.read_text(encoding="utf-8", errors="ignore"))
                    result.append({
                        "id": item.name,
                        "title": meta.get("title", item.name[:12]),
                        "created_at": meta.get("created_at", ""),
                        "updated_at": meta.get("updated_at", ""),
                        "message_count": meta.get("message_count", 0),
                    })
                    count += 1
                except:
                    pass
            else:
                result.append({
                    "id": item.name,
                    "title": item.name[:16],
                    "created_at": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                    "updated_at": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    "message_count": 0,
                })
                count += 1
        
        # 格式2: JSON 文件格式 (session_*.json 或 *.jsonl)
        elif item.is_file() and (item.suffix == '.json' or item.suffix == '.jsonl'):
            name = item.stem
            # 跳过 request_dump 文件
            if name.startswith('request_dump'):
                continue
            
            try:
                # 尝试读取文件获取更多信息
                content = item.read_text(encoding="utf-8", errors="ignore")
                msg_count = content.count('"role"') if item.suffix == '.json' else content.count('\n')
                
                result.append({
                    "id": item.name,
                    "title": name[:30],
                    "created_at": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                    "updated_at": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    "message_count": max(0, msg_count // 2),  # 每条消息有 user 和 assistant
                })
                count += 1
            except:
                result.append({
                    "id": item.name,
                    "title": name[:30],
                    "created_at": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
                    "updated_at": datetime.fromtimestamp(item.stat().st_mtime).isoformat(),
                    "message_count": 0,
                })
                count += 1
    
    return result


def get_config() -> dict:
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
        "toolsets": cfg.get("toolsets", []),
    }


def update_config(updates: dict) -> dict:
    cfg = read_yaml_config()
    cfg.update(updates)
    write_yaml_config(cfg)
    return cfg


def get_logs(limit: int = 50) -> List[dict]:
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
    log_file = HERMES_DATA / "logs" / name
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8", errors="ignore")
        return "\n".join(content.split("\n")[-lines:])
    return ""


def get_usage() -> dict:
    usage_file = HERMES_DATA / "model_usage.json"
    return read_json(usage_file) or {}


def get_workflows() -> list:
    wf = read_json(HERMES_DATA / "workflows.json")
    return wf if isinstance(wf, list) else []


def get_state_db_stats() -> dict:
    """从 state.db 获取统计信息"""
    db_path = HERMES_DATA / "state.db"
    if not db_path.exists():
        return {}
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
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


def get_all_models() -> dict:
    free_models = read_json(HERMES_DATA / "free_models.json") or {}
    models = free_models.get("models", []) if isinstance(free_models, dict) else []
    cfg = read_yaml_config()
    current = cfg.get("model", {})
    
    return {
        "current": current,
        "free_models": models[:50],
        "total_free": len(models),
    }
