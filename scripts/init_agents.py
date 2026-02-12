#!/usr/bin/env python3
"""
初始化多智能体团队工作目录和基础文件

用法:
    python init_agents.py [--base-path /workspace/agents]
    
提示词配置存储在 agent_souls.json 中，方便管理和观察。
"""

import os
import json
import argparse

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOULS_FILE = os.path.join(SCRIPT_DIR, "agent_souls.json")


def load_agent_souls():
    """从 JSON 文件加载智能体配置"""
    if not os.path.exists(SOULS_FILE):
        raise FileNotFoundError(f"配置文件不存在: {SOULS_FILE}")
    
    with open(SOULS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def create_agent_workspace(base_path: str, agent_id: str, agent_info: dict):
    """为单个智能体创建工作目录和基础文件"""
    agent_path = os.path.join(base_path, agent_id)
    os.makedirs(agent_path, exist_ok=True)
    
    # 创建 SOUL.md
    soul_path = os.path.join(agent_path, "SOUL.md")
    with open(soul_path, "w", encoding="utf-8") as f:
        f.write(agent_info["soul"])
    
    # 创建 AGENTS.md
    agents_path = os.path.join(agent_path, "AGENTS.md")
    with open(agents_path, "w", encoding="utf-8") as f:
        f.write(f"""# AGENTS.md - {agent_info['name']} {agent_info['emoji']}

## 角色
你是智能体团队中的 {agent_info['name']}。

## 工作规范
1. 专注于你的专业领域
2. 输出结构化、可用的结果
3. 如果任务超出能力范围，明确说明

## 输出格式
- 使用 Markdown 格式
- 重要信息用标题和列表组织
- 代码用代码块包裹
""")
    
    print(f"  ✅ {agent_info['emoji']} {agent_id} ({agent_info['name']})")


def main():
    parser = argparse.ArgumentParser(description="初始化多智能体团队工作目录")
    parser.add_argument(
        "--base-path",
        default="/workspace/agents",
        help="智能体工作目录的基础路径 (default: /workspace/agents)"
    )
    parser.add_argument(
        "--agent",
        help="只初始化指定的智能体 (可选)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用的智能体"
    )
    args = parser.parse_args()
    
    # 加载配置
    try:
        agents = load_agent_souls()
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        return 1
    
    # 列出模式
    if args.list:
        print("\n📋 可用智能体列表:\n")
        for agent_id, agent_info in agents.items():
            print(f"  {agent_info['emoji']} {agent_id:12} - {agent_info['name']}")
        print(f"\n共 {len(agents)} 个智能体")
        print(f"配置文件: {SOULS_FILE}")
        return 0
    
    # 初始化模式
    if args.agent:
        # 只初始化指定智能体
        if args.agent not in agents:
            print(f"❌ 错误: 未找到智能体 '{args.agent}'")
            print(f"   可用: {', '.join(agents.keys())}")
            return 1
        
        print(f"\n🚀 初始化智能体: {args.agent}")
        print(f"   路径: {args.base_path}\n")
        
        os.makedirs(args.base_path, exist_ok=True)
        create_agent_workspace(args.base_path, args.agent, agents[args.agent])
        
        print(f"\n✨ 完成！")
    else:
        # 初始化所有智能体
        print(f"\n🚀 初始化多智能体团队工作目录")
        print(f"   路径: {args.base_path}")
        print(f"   配置: {SOULS_FILE}\n")
        
        os.makedirs(args.base_path, exist_ok=True)
        
        for agent_id, agent_info in agents.items():
            create_agent_workspace(args.base_path, agent_id, agent_info)
        
        print(f"\n✨ 完成！共创建 {len(agents)} 个智能体工作目录")
    
    print(f"\n下一步:")
    print(f"  1. 在 openclaw.json 中添加智能体配置")
    print(f"  2. 运行 `openclaw gateway restart` 重启服务")
    print(f"  3. 运行 `openclaw agents list` 验证配置")
    
    return 0


if __name__ == "__main__":
    exit(main())
