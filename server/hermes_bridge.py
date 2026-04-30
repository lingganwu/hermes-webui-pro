import os
import json
import asyncio
import subprocess
import yaml
from pathlib import Path

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))

def get_hermes_home() -> Path:
    return Path(HERMES_HOME)

async def run_hermes_command(args: list[str], timeout: int = 30) -> dict:
    """Execute a hermes CLI command and return stdout."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "hermes", *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        return {
            "exit_code": proc.returncode,
            "stdout": stdout.decode("utf-8", errors="replace").strip(),
            "stderr": stderr.decode("utf-8", errors="replace").strip(),
        }
    except asyncio.TimeoutError:
        return {"exit_code": -1, "stdout": "", "stderr": "Command timed out"}
    except FileNotFoundError:
        return {"exit_code": -1, "stdout": "", "stderr": "hermes command not found"}

async def chat_send(message: str, model: str = None) -> str:
    """Send a chat message via hermes CLI."""
    args = ["chat", "-q", message]
    if model:
        args.extend(["--model", model])
    result = await run_hermes_command(args, timeout=120)
    if result["exit_code"] == 0:
        return result["stdout"]
    return f"Error: {result['stderr'] or 'Unknown error'}"

def read_memory_file(filename: str) -> str:
    """Read a memory file from ~/.hermes/memory/."""
    path = get_hermes_home() / "memory" / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

def write_memory_file(filename: str, content: str):
    """Write to a memory file."""
    path = get_hermes_home() / "memory" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def get_memory_entries() -> list[dict]:
    """Get all memory entries."""
    mem_dir = get_hermes_home() / "memory"
    entries = []
    if mem_dir.exists():
        for f in sorted(mem_dir.iterdir()):
            if f.is_file() and f.suffix in ('.md', '.txt', '.json'):
                content = f.read_text(encoding="utf-8")
                entries.append({
                    "id": f.stem,
                    "filename": f.name,
                    "content": content,
                    "source": "file",
                    "size": f.stat().st_size,
                    "modified": f.stat().st_mtime,
                })
    return entries

def get_skills_list() -> list[dict]:
    """List all skills from ~/.hermes/skills/."""
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
                    # Parse frontmatter
                    if text.startswith("---"):
                        parts = text.split("---", 2)
                        if len(parts) >= 3:
                            try:
                                meta = yaml.safe_load(parts[1])
                                desc = meta.get("description", "")
                                tags = meta.get("tags", [])
                            except: pass
                    if not desc:
                        # First non-empty line after frontmatter
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
            if f.suffix == ".json":
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    sessions.append({
                        "id": f.stem,
                        "title": data.get("title", f.stem),
                        "messageCount": len(data.get("messages", [])),
                        "model": data.get("model", ""),
                        "createdAt": data.get("createdAt", f.stat().st_ctime),
                        "updatedAt": data.get("updatedAt", f.stat().st_mtime),
                    })
                except:
                    sessions.append({"id": f.stem, "title": f.stem, "messageCount": 0})
    return sessions[:50]

def get_session_messages(session_id: str) -> list[dict]:
    """Get messages from a session file."""
    path = get_hermes_home() / "sessions" / f"{session_id}.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("messages", [])
        except: pass
    return []
