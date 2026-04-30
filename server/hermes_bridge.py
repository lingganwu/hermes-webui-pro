import os
import json
import asyncio
import httpx
import yaml
from pathlib import Path

HERMES_HOME = os.environ.get("HERMES_HOME", "/opt/data")
HERMES_API_URL = os.environ.get("HERMES_API_URL", "http://host.docker.internal:8642")
HERMES_API_KEY = os.environ.get("HERMES_API_KEY", "2ce902868681037446986e161fa14d7a8b0b7f09ab2e7184d5330df23d23dd764099bf8c6d755482146735b88e9b58ab56839aad625b10f2d2bdf352305c0160")

def get_hermes_home() -> Path:
    return Path(HERMES_HOME)

def _api_headers() -> dict:
    return {"Authorization": f"Bearer {HERMES_API_KEY}", "Content-Type": "application/json"}

async def chat_send(message: str, model: str = None) -> str:
    """Send a chat message via Hermes HTTP API."""
    async with httpx.AsyncClient(timeout=120) as client:
        # Step 1: Start a run
        payload = {"input": message}
        if model:
            payload["model"] = model
        
        resp = await client.post(f"{HERMES_API_URL}/v1/runs", json=payload, headers=_api_headers())
        if resp.status_code not in (200, 202):
            return f"Error: API returned {resp.status_code}"
        
        run_id = resp.json().get("run_id")
        if not run_id:
            return "Error: No run_id returned"
        
        # Step 2: Stream events until completion
        async with client.stream("GET", f"{HERMES_API_URL}/v1/runs/{run_id}/events", headers=_api_headers(), timeout=120) as events_resp:
            full_response = ""
            async for line in events_resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                try:
                    event = json.loads(line[6:])
                except:
                    continue
                
                event_type = event.get("event", "")
                
                if event_type == "message.delta":
                    full_response += event.get("delta", "")
                elif event_type == "run.completed":
                    output = event.get("output", "")
                    return output if output else full_response
                elif event_type == "run.error":
                    return f"Error: {event.get('error', 'Unknown')}"
            
            return full_response if full_response else "Error: No response received"

def get_memory_entries() -> list[dict]:
    """Get memory entries from SOUL.md and config."""
    entries = []
    
    soul_path = get_hermes_home() / "SOUL.md"
    if soul_path.exists():
        content = soul_path.read_text(encoding="utf-8")
        sections = content.split("\n## ")
        for i, section in enumerate(sections):
            if section.strip():
                lines = section.strip().split("\n", 1)
                title = lines[0].strip().lstrip("#").strip()
                body = lines[1].strip() if len(lines) > 1 else ""
                entries.append({
                    "id": f"soul_{i}",
                    "content": f"## {title}\n{body}" if body else f"## {title}",
                    "source": "SOUL.md",
                    "size": len(body),
                    "modified": soul_path.stat().st_mtime,
                })
    
    config = get_config()
    memory_config = config.get("memory", {})
    if memory_config.get("memory_enabled"):
        entries.append({
            "id": "memory_config",
            "content": f"Memory enabled: {memory_config.get('memory_enabled', False)}\nChar limit: {memory_config.get('memory_char_limit', 2200)}",
            "source": "config.yaml",
            "size": 100,
            "modified": 0,
        })
    
    return entries

def write_memory_content(content: str):
    """Write to SOUL.md."""
    soul_path = get_hermes_home() / "SOUL.md"
    soul_path.write_text(content, encoding="utf-8")

def get_skills_list() -> list[dict]:
    """List all skills."""
    skills_dir = get_hermes_home() / "skills"
    skills = []
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir():
                skill_md = d / "SKILL.md"
                desc = ""
                tags = []
                if skill_md.exists():
                    text = skill_md.read_text(encoding="utf-8")
                    if text.startswith("---"):
                        parts = text.split("---", 2)
                        if len(parts) >= 3:
                            try:
                                meta = yaml.safe_load(parts[1])
                                desc = meta.get("description", "")
                                tags = meta.get("tags", [])
                            except: pass
                    if not desc:
                        for line in text.split("\n"):
                            line = line.strip()
                            if line and not line.startswith("#") and not line.startswith("---"):
                                desc = line[:200]
                                break
                skills.append({"name": d.name, "description": desc, "tags": tags})
    return skills

def get_config() -> dict:
    """Read hermes config."""
    config_path = get_hermes_home() / "config.yaml"
    if config_path.exists():
        try:
            return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except:
            return {}
    return {}

def get_sessions_list() -> list[dict]:
    """List chat sessions."""
    sess_dir = get_hermes_home() / "sessions"
    sessions = []
    if sess_dir.exists():
        for f in sorted(sess_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.suffix == ".jsonl":
                try:
                    lines = f.read_text(encoding="utf-8").strip().split("\n")
                    meta = json.loads(lines[0]) if lines else {}
                    msg_count = sum(1 for l in lines[1:] if l.strip() and json.loads(l).get("role") in ("user", "assistant"))
                    sessions.append({
                        "id": f.stem,
                        "title": meta.get("title", f.stem.replace("_", " ")[:30]),
                        "messageCount": msg_count,
                        "model": meta.get("model", ""),
                        "createdAt": f.stat().st_ctime,
                        "updatedAt": f.stat().st_mtime,
                    })
                except:
                    sessions.append({"id": f.stem, "title": f.stem, "messageCount": 0})
    return sessions[:50]

def get_session_messages(session_id: str) -> list[dict]:
    """Get messages from a .jsonl session file."""
    path = get_hermes_home() / "sessions" / f"{session_id}.jsonl"
    messages = []
    if path.exists():
        try:
            lines = path.read_text(encoding="utf-8").strip().split("\n")
            for line in lines[1:]:
                if not line.strip():
                    continue
                entry = json.loads(line)
                role = entry.get("role", "")
                if role in ("user", "assistant", "system"):
                    content = entry.get("content", "")
                    if isinstance(content, list):
                        content = " ".join(
                            item.get("text", "") for item in content 
                            if isinstance(item, dict) and item.get("type") == "text"
                        )
                    messages.append({
                        "role": role,
                        "content": str(content),
                        "timestamp": entry.get("timestamp", 0),
                    })
        except:
            pass
    return messages
