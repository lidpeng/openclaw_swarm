#!/usr/bin/env python3
"""
Agent Swarm 配置向导
用于检测当前 OpenClaw 配置的模型，并帮助用户配置智能体团队
"""

import json
import os
import sys
from pathlib import Path

# OpenClaw 配置文件路径
CONFIG_PATHS = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path("/root/.openclaw/openclaw.json"),
]

# 智能体角色定义
AGENT_ROLES = {
    "pm": {"name": "产品经理", "emoji": "📋", "tier": "mid", "desc": "需求分析、任务拆解"},
    "researcher": {"name": "研究员", "emoji": "🔍", "tier": "low", "desc": "信息搜集、资料整理"},
    "coder": {"name": "程序员", "emoji": "👨‍💻", "tier": "high", "desc": "编码、调试、测试"},
    "writer": {"name": "写作者", "emoji": "✍️", "tier": "high", "desc": "文档、报告、文案"},
    "designer": {"name": "设计师", "emoji": "🎨", "tier": "mid", "desc": "配图、插画（需图像模型）"},
    "analyst": {"name": "分析师", "emoji": "📊", "tier": "high", "desc": "数据处理、统计分析"},
    "reviewer": {"name": "审核员", "emoji": "🔎", "tier": "high", "desc": "代码审查、内容审核"},
    "assistant": {"name": "助手", "emoji": "💬", "tier": "low", "desc": "简单问答、消息转发"},
    "automator": {"name": "自动化", "emoji": "🤖", "tier": "high", "desc": "定时任务、网页自动化"},
    "github-tracker": {"name": "GitHub追踪", "emoji": "🔥", "tier": "low", "desc": "热门项目追踪"},
}

# 主流模型推荐配置
RECOMMENDED_MODELS = {
    "claude-opus-4": {
        "name": "Claude Opus 4 / 4.5",
        "provider": "anthropic",
        "tier": "high",
        "desc": "最强综合能力，适合复杂任务",
        "api": "anthropic-messages",
        "example_config": {
            "baseUrl": "https://api.anthropic.com/v1",
            "api": "anthropic-messages",
            "authHeader": "x-api-key"
        }
    },
    "claude-sonnet-4": {
        "name": "Claude Sonnet 4",
        "provider": "anthropic",
        "tier": "mid",
        "desc": "性价比高，适合中等复杂度任务",
        "api": "anthropic-messages",
        "example_config": {
            "baseUrl": "https://api.anthropic.com/v1",
            "api": "anthropic-messages",
            "authHeader": "x-api-key"
        }
    },
    "gemini-2.5-pro": {
        "name": "Gemini 2.5 Pro",
        "provider": "google",
        "tier": "mid",
        "desc": "长上下文，适合文档处理",
        "api": "google-generative-ai",
        "example_config": {
            "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
            "api": "google-generative-ai",
            "authHeader": "x-goog-api-key"
        }
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "provider": "openai",
        "tier": "high",
        "desc": "OpenAI 旗舰模型",
        "api": "openai-completions",
        "example_config": {
            "baseUrl": "https://api.openai.com/v1",
            "api": "openai-completions",
            "authHeader": "Authorization"
        }
    },
    "deepseek-v3": {
        "name": "DeepSeek V3",
        "provider": "deepseek",
        "tier": "mid",
        "desc": "高性价比，中文优秀",
        "api": "openai-completions",
        "example_config": {
            "baseUrl": "https://api.deepseek.com/v1",
            "api": "openai-completions",
            "authHeader": "Authorization"
        }
    },
    "qwen-max": {
        "name": "Qwen Max",
        "provider": "alibaba",
        "tier": "mid",
        "desc": "阿里云通义千问，中文强",
        "api": "openai-completions",
        "example_config": {
            "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api": "openai-completions",
            "authHeader": "Authorization"
        }
    },
    "glm-4": {
        "name": "GLM-4",
        "provider": "zhipu",
        "tier": "low",
        "desc": "智谱清言，成本低",
        "api": "openai-completions",
        "example_config": {
            "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
            "api": "openai-completions",
            "authHeader": "Authorization"
        }
    }
}


def load_openclaw_config():
    """加载 OpenClaw 配置文件"""
    for config_path in CONFIG_PATHS:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f), config_path
    return None, None


def get_available_models(config):
    """从配置中提取可用模型列表"""
    models = []
    if not config or 'models' not in config:
        return models
    
    providers = config.get('models', {}).get('providers', {})
    for provider_id, provider_config in providers.items():
        for model in provider_config.get('models', []):
            model_id = model.get('id', '')
            model_name = model.get('name', model_id)
            full_id = f"{provider_id}/{model_id}"
            
            # 判断模型能力等级
            tier = "mid"
            model_lower = model_id.lower()
            if any(x in model_lower for x in ['opus', 'gpt-4', 'pro']):
                tier = "high"
            elif any(x in model_lower for x in ['glm', 'flash', 'mini']):
                tier = "low"
            
            # 检测是否支持图像
            supports_image = 'image' in model.get('input', [])
            
            models.append({
                'full_id': full_id,
                'provider_id': provider_id,
                'model_id': model_id,
                'name': model_name,
                'tier': tier,
                'supports_image': supports_image,
                'reasoning': model.get('reasoning', False),
                'context_window': model.get('contextWindow', 0)
            })
    
    return models


def print_current_models(models):
    """打印当前可用模型"""
    print("\n" + "="*60)
    print("📦 当前 OpenClaw 已配置的模型")
    print("="*60)
    
    if not models:
        print("⚠️  未检测到任何已配置的模型")
        return
    
    # 按等级分组
    high_tier = [m for m in models if m['tier'] == 'high']
    mid_tier = [m for m in models if m['tier'] == 'mid']
    low_tier = [m for m in models if m['tier'] == 'low']
    
    def print_model_group(title, model_list):
        if model_list:
            print(f"\n{title}")
            for i, m in enumerate(model_list, 1):
                img_tag = "🖼️" if m['supports_image'] else ""
                reason_tag = "🧠" if m['reasoning'] else ""
                ctx = f"({m['context_window']//1000}k)" if m['context_window'] else ""
                print(f"  {i}. {m['name']} {img_tag}{reason_tag} {ctx}")
                print(f"     ID: {m['full_id']}")
    
    print_model_group("🔴 高性能模型 (High Tier)", high_tier)
    print_model_group("🟡 中等模型 (Mid Tier)", mid_tier)
    print_model_group("🟢 轻量模型 (Low Tier)", low_tier)
    
    print("\n" + "-"*60)
    print("图例: 🖼️=支持图像 🧠=支持推理")


def suggest_model_assignment(models):
    """根据现有模型建议智能体分配"""
    print("\n" + "="*60)
    print("🤖 智能体模型分配建议")
    print("="*60)
    
    # 按等级分类模型
    high_models = [m for m in models if m['tier'] == 'high']
    mid_models = [m for m in models if m['tier'] == 'mid']
    low_models = [m for m in models if m['tier'] == 'low']
    image_models = [m for m in models if m['supports_image']]
    
    # 选择每个等级的首选模型
    best_high = high_models[0]['full_id'] if high_models else None
    best_mid = mid_models[0]['full_id'] if mid_models else best_high
    best_low = low_models[0]['full_id'] if low_models else best_mid
    
    # 图像模型优先选择名字中带 "image" 的
    image_priority = [m for m in image_models if 'image' in m['model_id'].lower()]
    best_image = image_priority[0]['full_id'] if image_priority else (image_models[0]['full_id'] if image_models else best_mid)
    
    print("\n根据您的模型配置，建议分配如下：\n")
    
    assignments = {}
    for agent_id, agent_info in AGENT_ROLES.items():
        tier = agent_info['tier']
        
        if agent_id == 'designer':
            suggested = best_image
        elif tier == 'high':
            suggested = best_high
        elif tier == 'mid':
            suggested = best_mid
        else:
            suggested = best_low
        
        if suggested:
            assignments[agent_id] = suggested
            print(f"  {agent_info['emoji']} {agent_info['name']:8} → {suggested}")
            print(f"     ({agent_info['desc']})")
    
    return assignments


def generate_config_patch(assignments):
    """生成配置补丁"""
    agents_list = []
    
    # main agent
    agents_list.append({
        "id": "main",
        "default": True,
        "workspace": "/workspace",
        "identity": {"name": "主智能体", "emoji": "🎯"},
        "subagents": {"allowAgents": list(AGENT_ROLES.keys())}
    })
    
    # sub agents
    for agent_id, model_id in assignments.items():
        agent_info = AGENT_ROLES[agent_id]
        agents_list.append({
            "id": agent_id,
            "workspace": f"/workspace/agents/{agent_id}",
            "model": {"primary": model_id},
            "identity": {"name": agent_info['name'], "emoji": agent_info['emoji']}
        })
    
    return {"agents": {"list": agents_list}}


def main():
    """主函数"""
    print("\n" + "🚀 Agent Swarm 配置向导".center(60))
    print("="*60)
    
    # 1. 加载配置
    config, config_path = load_openclaw_config()
    if config:
        print(f"✅ 已加载配置文件: {config_path}")
    else:
        print("❌ 未找到 OpenClaw 配置文件")
        print("   请确保 ~/.openclaw/openclaw.json 存在")
        return
    
    # 2. 获取可用模型
    models = get_available_models(config)
    print_current_models(models)
    
    if not models:
        print("\n💡 您需要先配置模型才能使用 Agent Swarm")
        print("   可选的主流模型：")
        for model_id, info in RECOMMENDED_MODELS.items():
            print(f"   - {info['name']}: {info['desc']}")
        return
    
    # 3. 建议分配
    assignments = suggest_model_assignment(models)
    
    # 4. 输出配置补丁
    print("\n" + "="*60)
    print("📝 生成的配置补丁 (可用于 gateway config.patch)")
    print("="*60)
    
    patch = generate_config_patch(assignments)
    print(json.dumps(patch, indent=2, ensure_ascii=False))
    
    # 5. 保存到文件
    output_path = Path(__file__).parent.parent / "config-patch.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patch, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 配置已保存到: {output_path}")
    
    print("\n" + "="*60)
    print("下一步操作：")
    print("  1. 检查上方配置是否符合预期")
    print("  2. 如需修改，编辑 config-patch.json")
    print("  3. 使用 gateway config.patch 应用配置")
    print("="*60)


if __name__ == "__main__":
    main()
