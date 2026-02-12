#!/usr/bin/env python3
"""
Agent Swarm 强制入口脚本

所有智能体集群操作必须先通过此入口，确保配置检查不被跳过。

用法:
    python3 scripts/swarm_entry.py [--action init|reset|status]

返回 JSON 格式，根据 status 字段决定下一步：
- "need_config" → 向用户展示 display 内容，等待选择
- "ready" → 直接进入任务编排
- "init_success" → 初始化完成
- "reset_success" → 重置完成
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# 路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SKILL_DIR, ".swarm-config.json")

# 默认智能体列表
DEFAULT_AGENTS = [
    {"id": "pm", "emoji": "📋", "name": "产品经理", "role": "规划者", "model_tier": "medium"},
    {"id": "researcher", "emoji": "🔍", "name": "研究员", "role": "信息猎手", "model_tier": "light"},
    {"id": "coder", "emoji": "👨‍💻", "name": "程序员", "role": "代码工匠", "model_tier": "high"},
    {"id": "writer", "emoji": "✍️", "name": "写作者", "role": "文字工匠", "model_tier": "high"},
    {"id": "designer", "emoji": "🎨", "name": "设计师", "role": "视觉创作者", "model_tier": "image"},
    {"id": "analyst", "emoji": "📊", "name": "分析师", "role": "数据侦探", "model_tier": "high"},
    {"id": "reviewer", "emoji": "🔎", "name": "审核员", "role": "质量守门人", "model_tier": "high"},
    {"id": "assistant", "emoji": "💬", "name": "助手", "role": "沟通桥梁", "model_tier": "light"},
    {"id": "automator", "emoji": "🤖", "name": "自动化", "role": "效率大师", "model_tier": "high"},
]

# 模型等级说明
MODEL_TIERS = {
    "high": "🔴 高性能模型 (Claude Opus 等)",
    "medium": "🟡 中等模型 (Gemini Pro 等)",
    "light": "🟢 轻量模型 (GLM-4 等)",
    "image": "🖼️ 图像模型 (Gemini Image 等)",
}


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"initialized": False}


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def is_initialized():
    """检查是否已初始化"""
    config = load_config()
    return config.get("initialized", False)


def detect_models():
    """
    检测 OpenClaw 已配置的模型
    返回按等级分类的模型列表
    """
    # 尝试读取 openclaw.json 配置
    possible_paths = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        "/root/.openclaw/openclaw.json",
    ]
    
    models = {
        "high": [],
        "medium": [],
        "light": [],
        "image": [],
    }
    
    for config_path in possible_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                providers = config.get("models", {}).get("providers", {})
                
                for provider_id, provider_config in providers.items():
                    provider_models = provider_config.get("models", [])
                    for model in provider_models:
                        model_id = model.get("id", "")
                        model_name = model.get("name", model_id)
                        full_id = f"{provider_id}/{model_id}"
                        
                        model_info = {
                            "id": full_id,
                            "name": model_name,
                            "provider": provider_id,
                        }
                        
                        # 按模型名称分类
                        name_lower = model_name.lower()
                        id_lower = model_id.lower()
                        
                        if "image" in name_lower or "image" in id_lower:
                            models["image"].append(model_info)
                        elif any(x in name_lower for x in ["opus", "gpt-4", "claude-4"]):
                            models["high"].append(model_info)
                        elif any(x in name_lower for x in ["sonnet", "gemini", "pro"]):
                            models["medium"].append(model_info)
                        elif any(x in name_lower for x in ["glm", "deepseek", "qwen"]):
                            models["light"].append(model_info)
                        else:
                            models["medium"].append(model_info)  # 默认中等
                
                break  # 找到配置就停止
            except Exception as e:
                pass
    
    return models


def format_models_display(models):
    """格式化模型展示内容"""
    lines = ["## 📦 您的 OpenClaw 已配置以下模型\n"]
    
    tier_order = [
        ("high", "### 🔴 高性能模型 (适合: coder, writer, analyst, reviewer)"),
        ("medium", "### 🟡 中等模型 (适合: pm, designer)"),
        ("light", "### 🟢 轻量模型 (适合: researcher, assistant)"),
        ("image", "### 🖼️ 图像模型 (适合: designer)"),
    ]
    
    for tier, header in tier_order:
        if models.get(tier):
            lines.append(header)
            for m in models[tier]:
                lines.append(f"- {m['name']} (`{m['id']}`)")
            lines.append("")
    
    if not any(models.values()):
        lines.append("⚠️ 未检测到已配置的模型，请先在 openclaw.json 中添加模型配置。")
    
    return "\n".join(lines)


def format_config_prompt():
    """格式化配置提示"""
    return """请选择配置方式：

**A. 自动分配** — 根据您现有的模型自动配置智能体团队
   - 高性能任务(编码/写作/分析) → 使用您最强的模型
   - 中等任务(规划/设计) → 使用中等模型
   - 轻量任务(搜索/问答) → 使用成本最低的模型

**B. 添加新模型** — 我会推荐主流模型供您选择

**C. 自定义配置** — 您手动指定每个智能体的模型

请回复 A/B/C 或直接告诉我您的选择。"""


def get_available_agents():
    """获取可用智能体列表"""
    config = load_config()
    agents = config.get("agents", DEFAULT_AGENTS)
    return agents


def do_init(model_mapping=None):
    """执行初始化"""
    config = {
        "initialized": True,
        "version": "1.0.0",
        "configuredAt": datetime.now().isoformat(),
        "agents": DEFAULT_AGENTS,
        "modelMapping": model_mapping or {},
    }
    save_config(config)
    return config


def do_reset():
    """重置配置"""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    return True


def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Swarm 强制入口")
    parser.add_argument("--action", choices=["check", "init", "reset", "status"],
                       default="check", help="操作类型")
    parser.add_argument("--model-mapping", type=str, help="模型映射 JSON 字符串")
    
    args = parser.parse_args()
    
    result = {}
    
    if args.action == "check":
        if is_initialized():
            # 已初始化，返回 ready 状态
            result = {
                "status": "ready",
                "message": "Agent Swarm 已就绪，可以开始任务编排",
                "agents": get_available_agents(),
            }
        else:
            # 未初始化，返回 need_config 状态
            models = detect_models()
            result = {
                "status": "need_config",
                "message": "Agent Swarm 尚未初始化，请先完成配置",
                "display": format_models_display(models),
                "prompt": format_config_prompt(),
                "detected_models": models,
            }
    
    elif args.action == "init":
        model_mapping = {}
        if args.model_mapping:
            try:
                model_mapping = json.loads(args.model_mapping)
            except:
                pass
        
        config = do_init(model_mapping)
        result = {
            "status": "init_success",
            "message": "Agent Swarm 初始化完成",
            "config": config,
        }
    
    elif args.action == "reset":
        do_reset()
        result = {
            "status": "reset_success",
            "message": "配置已重置，下次使用时将重新运行配置向导",
        }
    
    elif args.action == "status":
        config = load_config()
        result = {
            "status": "initialized" if config.get("initialized") else "not_initialized",
            "config": config,
        }
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
