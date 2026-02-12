#!/usr/bin/env python3
"""
智能体经验记录工具

用于在任务完成后记录经验，供后续任务参考。

用法:
    python experience_logger.py log <agent_id> "经验描述" --task "任务名称"
    python experience_logger.py show <agent_id>
    python experience_logger.py summary <agent_id>  # 生成经验摘要
    python experience_logger.py inject <agent_id>   # 输出可注入到 prompt 的经验
"""

import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DEFAULT_AGENTS_PATH = "/workspace/agents"
MAX_EXPERIENCES = 50  # 每个智能体最多保留的经验数


def get_experience_file(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> Path:
    return Path(base_path) / agent_id / "memory" / "experience.md"


def get_experience_json(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> Path:
    return Path(base_path) / agent_id / "memory" / "experience.json"


def log_experience(agent_id: str, experience: str, task: str = None, 
                   category: str = "general", base_path: str = DEFAULT_AGENTS_PATH) -> dict:
    """记录一条经验"""
    exp_file = get_experience_file(agent_id, base_path)
    exp_json = get_experience_json(agent_id, base_path)
    
    # 确保目录存在
    exp_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 当前时间
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    # 记录到 JSON（结构化）
    experiences = []
    if exp_json.exists():
        try:
            experiences = json.loads(exp_json.read_text())
        except:
            experiences = []
    
    new_exp = {
        "id": f"exp_{now.strftime('%Y%m%d%H%M%S')}",
        "content": experience,
        "task": task,
        "category": category,
        "created": now.isoformat(),
        "used_count": 0
    }
    experiences.append(new_exp)
    
    # 保留最近 MAX_EXPERIENCES 条
    if len(experiences) > MAX_EXPERIENCES:
        experiences = experiences[-MAX_EXPERIENCES:]
    
    exp_json.write_text(json.dumps(experiences, indent=2, ensure_ascii=False))
    
    # 同时更新 Markdown 文件（人类可读）
    task_info = f" ({task})" if task else ""
    new_line = f"- [{date_str}] {experience}{task_info}\n"
    
    if exp_file.exists():
        content = exp_file.read_text()
        # 在 "## 经验记录" 后插入
        if "## 经验记录" in content:
            parts = content.split("## 经验记录")
            # 移除 "(暂无记录)" 提示
            rest = parts[1].replace("*(暂无记录)*\n", "").replace("*(暂无记录)*", "")
            content = parts[0] + "## 经验记录\n\n" + new_line + rest.lstrip('\n')
            exp_file.write_text(content)
    else:
        # 创建新文件
        content = f"""# 经验记忆 - {agent_id}

*记录执行任务中获得的有效经验*

## 经验记录

{new_line}
"""
        exp_file.write_text(content)
    
    return {
        "success": True,
        "agent_id": agent_id,
        "experience_id": new_exp["id"],
        "total_experiences": len(experiences)
    }


def show_experiences(agent_id: str, limit: int = 10, base_path: str = DEFAULT_AGENTS_PATH) -> list:
    """查看智能体的经验记录"""
    exp_json = get_experience_json(agent_id, base_path)
    
    if not exp_json.exists():
        return []
    
    try:
        experiences = json.loads(exp_json.read_text())
        return experiences[-limit:]  # 返回最近 N 条
    except:
        return []


def generate_summary(agent_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> str:
    """生成经验摘要（按类别分组）"""
    experiences = show_experiences(agent_id, limit=50, base_path=base_path)
    
    if not experiences:
        return "暂无经验记录"
    
    # 按类别分组
    by_category = defaultdict(list)
    for exp in experiences:
        cat = exp.get("category", "general")
        by_category[cat].append(exp["content"])
    
    # 生成摘要
    lines = [f"## {agent_id} 经验摘要\n"]
    for cat, exps in by_category.items():
        lines.append(f"### {cat}")
        for exp in exps[-5:]:  # 每类最多 5 条
            lines.append(f"- {exp}")
        lines.append("")
    
    return "\n".join(lines)


def inject_experiences(agent_id: str, limit: int = 5, base_path: str = DEFAULT_AGENTS_PATH) -> str:
    """
    输出可注入到 prompt 的经验片段
    用于在 spawn 时注入相关经验
    """
    experiences = show_experiences(agent_id, limit=limit, base_path=base_path)
    
    if not experiences:
        return ""
    
    lines = ["## 历史经验（供参考）\n"]
    for exp in experiences:
        task_info = f" (来自: {exp['task']})" if exp.get('task') else ""
        lines.append(f"- {exp['content']}{task_info}")
    
    return "\n".join(lines)


def mark_experience_used(agent_id: str, exp_id: str, base_path: str = DEFAULT_AGENTS_PATH) -> bool:
    """标记经验已被使用（用于统计有效性）"""
    exp_json = get_experience_json(agent_id, base_path)
    
    if not exp_json.exists():
        return False
    
    try:
        experiences = json.loads(exp_json.read_text())
        for exp in experiences:
            if exp.get("id") == exp_id:
                exp["used_count"] = exp.get("used_count", 0) + 1
                exp["last_used"] = datetime.now().isoformat()
        exp_json.write_text(json.dumps(experiences, indent=2, ensure_ascii=False))
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description="智能体经验记录工具")
    parser.add_argument("action", choices=["log", "show", "summary", "inject"])
    parser.add_argument("agent_id", help="智能体 ID")
    parser.add_argument("experience", nargs="?", help="经验描述（log 时必填）")
    parser.add_argument("--task", help="来源任务")
    parser.add_argument("--category", default="general", help="经验类别")
    parser.add_argument("--limit", type=int, default=10, help="显示数量")
    parser.add_argument("--base-path", default=DEFAULT_AGENTS_PATH)
    
    args = parser.parse_args()
    
    if args.action == "log":
        if not args.experience:
            print("错误: log 操作需要提供经验描述")
            return
        result = log_experience(
            args.agent_id, 
            args.experience, 
            task=args.task,
            category=args.category,
            base_path=args.base_path
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "show":
        experiences = show_experiences(args.agent_id, limit=args.limit, base_path=args.base_path)
        for exp in experiences:
            print(f"[{exp.get('created', '?')[:10]}] {exp['content']}")
    
    elif args.action == "summary":
        print(generate_summary(args.agent_id, args.base_path))
    
    elif args.action == "inject":
        print(inject_experiences(args.agent_id, limit=args.limit, base_path=args.base_path))


if __name__ == "__main__":
    main()
