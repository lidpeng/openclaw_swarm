#!/usr/bin/env python3
"""
智能体集群配置管理工具

用法:
    python agent_manager.py list                    # 列出所有智能体
    python agent_manager.py show <agent_id>         # 查看智能体详情
    python agent_manager.py add <agent_id>          # 添加新智能体
    python agent_manager.py remove <agent_id>       # 删除智能体
    python agent_manager.py update <agent_id>       # 更新智能体配置
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime

DEFAULT_AGENTS_PATH = "/workspace/agents"

AGENT_TEMPLATES = {
    "default": {
        "name": "新智能体",
        "emoji": "🤖",
        "model": "claude-opus-4",
        "tools_allow": ["read", "write"],
        "tools_deny": ["gateway", "message"],
        "soul": """# SOUL.md - {name}

_你的核心职责描述_

## 工作原则

1. **原则一** — 描述
2. **原则二** — 描述

## 边界

- ❌ 不做什么
- ✅ 专注于什么
"""
    },
    "researcher": {
        "name": "研究员",
        "emoji": "🔍",
        "model": "glm-4",
        "tools_allow": ["web_search", "web_fetch", "read", "write", "memory_search", "memory_get"],
        "tools_deny": ["exec", "process", "gateway", "browser", "message", "cron"]
    },
    "coder": {
        "name": "程序员",
        "emoji": "👨‍💻",
        "model": "claude-opus-4",
        "tools_allow": ["read", "write", "edit", "exec", "process"],
        "tools_deny": ["web_search", "browser", "message", "gateway", "cron"]
    },
    "writer": {
        "name": "写作者",
        "emoji": "✍️",
        "model": "gemini-2.5-pro",
        "tools_allow": ["read", "write", "edit", "memory_search", "memory_get"],
        "tools_deny": ["exec", "process", "browser", "gateway", "message", "cron"]
    }
}


def get_agent_path(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> Path:
    return Path(base_path) / agent_id


def list_agents(base_path: str = DEFAULT_AGENTS_PATH) -> list:
    """列出所有智能体"""
    agents = []
    base = Path(base_path)
    if not base.exists():
        return agents
    
    for agent_dir in base.iterdir():
        if agent_dir.is_dir() and not agent_dir.name.startswith('.'):
            soul_file = agent_dir / "SOUL.md"
            agents_file = agent_dir / "AGENTS.md"
            memory_file = agent_dir / "memory" / "experience.md"
            
            agent_info = {
                "id": agent_dir.name,
                "path": str(agent_dir),
                "has_soul": soul_file.exists(),
                "has_agents": agents_file.exists(),
                "has_memory": memory_file.exists(),
            }
            
            # 尝试读取名称和emoji
            if soul_file.exists():
                content = soul_file.read_text()
                if "# SOUL.md - " in content:
                    first_line = content.split('\n')[0]
                    agent_info["name"] = first_line.replace("# SOUL.md - ", "").strip()
            
            agents.append(agent_info)
    
    return agents


def show_agent(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> dict:
    """查看智能体详情"""
    agent_path = get_agent_path(agent_id, base_path)
    if not agent_path.exists():
        return {"error": f"智能体 {agent_id} 不存在"}
    
    info = {
        "id": agent_id,
        "path": str(agent_path),
        "files": []
    }
    
    for f in agent_path.iterdir():
        if f.is_file():
            info["files"].append(f.name)
        elif f.is_dir():
            info["files"].append(f"{f.name}/")
    
    # 读取 SOUL.md
    soul_file = agent_path / "SOUL.md"
    if soul_file.exists():
        info["soul"] = soul_file.read_text()[:500] + "..." if len(soul_file.read_text()) > 500 else soul_file.read_text()
    
    # 读取经验记忆
    memory_file = agent_path / "memory" / "experience.md"
    if memory_file.exists():
        info["experience"] = memory_file.read_text()
    
    return info


def add_agent(agent_id: str, template: str = "default", base_path: str = DEFAULT_AGENTS_PATH, **kwargs) -> dict:
    """添加新智能体"""
    agent_path = get_agent_path(agent_id, base_path)
    if agent_path.exists():
        return {"error": f"智能体 {agent_id} 已存在"}
    
    # 获取模板
    tmpl = AGENT_TEMPLATES.get(template, AGENT_TEMPLATES["default"]).copy()
    tmpl.update(kwargs)
    
    # 创建目录
    agent_path.mkdir(parents=True, exist_ok=True)
    (agent_path / "memory").mkdir(exist_ok=True)
    
    # 创建 SOUL.md
    soul_content = tmpl.get("soul", AGENT_TEMPLATES["default"]["soul"])
    soul_content = soul_content.format(name=tmpl.get("name", agent_id))
    (agent_path / "SOUL.md").write_text(soul_content)
    
    # 创建 AGENTS.md
    agents_content = f"""# AGENTS.md - {tmpl.get('name', agent_id)} {tmpl.get('emoji', '🤖')}

## 角色
你是智能体团队中的 {tmpl.get('name', agent_id)}。

## 可用工具
{chr(10).join(f"- `{t}`" for t in tmpl.get('tools_allow', []))}

## 工作规范
1. 专注于你的专业领域
2. 输出结构化、可用的结果
3. 任务完成后总结经验到 memory/experience.md
"""
    (agent_path / "AGENTS.md").write_text(agents_content)
    
    # 创建经验记忆文件
    experience_content = f"""# 经验记忆 - {tmpl.get('name', agent_id)}

*记录执行任务中获得的有效经验*

## 使用说明
每次完成任务后，总结 1-3 条简短经验，格式：
- [日期] 经验描述 (来源任务)

## 经验记录

*(暂无记录)*
"""
    (agent_path / "memory" / "experience.md").write_text(experience_content)
    
    return {
        "success": True,
        "agent_id": agent_id,
        "path": str(agent_path),
        "template": template
    }


def remove_agent(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH, backup: bool = True) -> dict:
    """删除智能体（默认先备份）"""
    agent_path = get_agent_path(agent_id, base_path)
    if not agent_path.exists():
        return {"error": f"智能体 {agent_id} 不存在"}
    
    if backup:
        import shutil
        backup_path = Path(base_path) / f".backup_{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(agent_path), str(backup_path))
        return {
            "success": True,
            "agent_id": agent_id,
            "backup_path": str(backup_path)
        }
    else:
        import shutil
        shutil.rmtree(agent_path)
        return {
            "success": True,
            "agent_id": agent_id,
            "deleted": True
        }


def update_agent(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH, **kwargs) -> dict:
    """更新智能体配置"""
    agent_path = get_agent_path(agent_id, base_path)
    if not agent_path.exists():
        return {"error": f"智能体 {agent_id} 不存在"}
    
    updated = []
    
    # 更新名称
    if "name" in kwargs:
        soul_file = agent_path / "SOUL.md"
        if soul_file.exists():
            content = soul_file.read_text()
            # 简单替换第一行
            lines = content.split('\n')
            if lines[0].startswith("# SOUL.md"):
                lines[0] = f"# SOUL.md - {kwargs['name']}"
                soul_file.write_text('\n'.join(lines))
                updated.append("name")
    
    # 更新 emoji
    if "emoji" in kwargs:
        agents_file = agent_path / "AGENTS.md"
        if agents_file.exists():
            content = agents_file.read_text()
            # 替换第一行的 emoji
            lines = content.split('\n')
            if lines[0].startswith("# AGENTS.md"):
                # 尝试更新 emoji
                updated.append("emoji")
    
    return {
        "success": True,
        "agent_id": agent_id,
        "updated": updated
    }


def main():
    parser = argparse.ArgumentParser(description="智能体集群配置管理")
    parser.add_argument("action", choices=["list", "show", "add", "remove", "update"])
    parser.add_argument("agent_id", nargs="?", help="智能体 ID")
    parser.add_argument("--base-path", default=DEFAULT_AGENTS_PATH, help="智能体目录")
    parser.add_argument("--template", default="default", help="模板 (default/researcher/coder/writer)")
    parser.add_argument("--name", help="智能体名称")
    parser.add_argument("--emoji", help="智能体 emoji")
    parser.add_argument("--no-backup", action="store_true", help="删除时不备份")
    
    args = parser.parse_args()
    
    if args.action == "list":
        agents = list_agents(args.base_path)
        print(f"\n📋 智能体列表 ({len(agents)} 个)\n")
        for a in agents:
            status = "✅" if a.get("has_soul") else "⚠️"
            memory = "🧠" if a.get("has_memory") else ""
            name = a.get("name", a["id"])
            print(f"  {status} {a['id']:12} {name} {memory}")
        print()
    
    elif args.action == "show":
        if not args.agent_id:
            print("错误: 需要指定 agent_id")
            return
        result = show_agent(args.agent_id, args.base_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "add":
        if not args.agent_id:
            print("错误: 需要指定 agent_id")
            return
        kwargs = {}
        if args.name:
            kwargs["name"] = args.name
        if args.emoji:
            kwargs["emoji"] = args.emoji
        result = add_agent(args.agent_id, args.template, args.base_path, **kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "remove":
        if not args.agent_id:
            print("错误: 需要指定 agent_id")
            return
        result = remove_agent(args.agent_id, args.base_path, backup=not args.no_backup)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "update":
        if not args.agent_id:
            print("错误: 需要指定 agent_id")
            return
        kwargs = {}
        if args.name:
            kwargs["name"] = args.name
        if args.emoji:
            kwargs["emoji"] = args.emoji
        result = update_agent(args.agent_id, args.base_path, **kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
