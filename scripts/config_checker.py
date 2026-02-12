#!/usr/bin/env python3
"""
Agent Swarm 配置状态检查器

用于检查和管理 Agent Swarm 的初始化状态。
"""

import os
import json
from datetime import datetime

# 配置文件路径（相对于 skill 目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SKILL_DIR, ".swarm-config.json")

DEFAULT_CONFIG = {
    "initialized": False,
    "version": "1.0.0",
    "configuredAt": None,
    "agents": [],
    "modelMapping": {}
}


def load_config():
    """加载配置文件，不存在则返回默认配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return True


def is_initialized():
    """检查是否已完成初始化配置"""
    config = load_config()
    return config.get("initialized", False)


def mark_initialized(agents=None, model_mapping=None):
    """标记为已初始化"""
    config = load_config()
    config["initialized"] = True
    config["configuredAt"] = datetime.now().isoformat()
    config["version"] = "1.0.0"
    
    if agents:
        config["agents"] = agents
    if model_mapping:
        config["modelMapping"] = model_mapping
    
    save_config(config)
    return config


def reset_config():
    """重置配置状态"""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return True


def get_status():
    """获取当前配置状态"""
    config = load_config()
    return {
        "initialized": config.get("initialized", False),
        "version": config.get("version", "unknown"),
        "configuredAt": config.get("configuredAt"),
        "agentCount": len(config.get("agents", [])),
        "configFile": CONFIG_FILE
    }


def main():
    """CLI 入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Swarm 配置状态检查器")
    parser.add_argument("action", choices=["check", "init", "reset", "status"],
                       help="操作类型: check(检查), init(初始化), reset(重置), status(状态)")
    parser.add_argument("--agents", nargs="+", help="智能体列表（init时使用）")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    if args.action == "check":
        initialized = is_initialized()
        if args.json:
            print(json.dumps({"initialized": initialized}))
        else:
            if initialized:
                print("✅ Agent Swarm 已完成初始化配置")
            else:
                print("⚠️ Agent Swarm 尚未初始化，请先运行配置向导")
        return 0 if initialized else 1
    
    elif args.action == "init":
        default_agents = ["pm", "researcher", "coder", "writer", "designer", 
                        "analyst", "reviewer", "assistant", "automator"]
        agents = args.agents or default_agents
        config = mark_initialized(agents=agents)
        if args.json:
            print(json.dumps(config, indent=2))
        else:
            print(f"✅ 已标记为初始化完成")
            print(f"   配置文件: {CONFIG_FILE}")
            print(f"   智能体数: {len(agents)}")
        return 0
    
    elif args.action == "reset":
        reset_config()
        if args.json:
            print(json.dumps({"reset": True}))
        else:
            print("✅ 配置已重置，下次使用时将重新运行配置向导")
        return 0
    
    elif args.action == "status":
        status = get_status()
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("📊 Agent Swarm 配置状态")
            print(f"   初始化: {'✅ 是' if status['initialized'] else '❌ 否'}")
            print(f"   版本: {status['version']}")
            print(f"   配置时间: {status['configuredAt'] or '未配置'}")
            print(f"   智能体数: {status['agentCount']}")
            print(f"   配置文件: {status['configFile']}")
        return 0


if __name__ == "__main__":
    exit(main())
