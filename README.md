<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=for-the-badge" alt="OpenClaw Skill"/>
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README_EN.md">🇺🇸 English</a>
</p>

---

# 🤖 Agent Swarm - 多智能体集群编排

> 将复杂任务拆解给专业智能体团队，并行协作高效完成

## ✨ 特性

- 🎯 **10+ 专业智能体** - PM、研究员、程序员、写作者、设计师、分析师等
- ⚡ **并行执行** - 无依赖任务同时运行，大幅提升效率
- 🧠 **智能调度** - 根据任务复杂度自动选择合适的模型
- 💰 **成本优化** - 简单任务用便宜模型，复杂任务用强模型
- 📝 **经验积累** - 智能体可记录和复用历史经验
- 🔧 **灵活配置** - 支持自定义智能体和模型分配

## 📦 智能体团队

| 智能体 | 角色 | 核心能力 |
|--------|------|----------|
| 📋 pm | 产品经理 | 需求分析、任务拆解、优先级排序 |
| 🔍 researcher | 研究员 | 信息搜集、资料整理、多源验证 |
| 👨‍💻 coder | 程序员 | 编码、调试、测试、重构 |
| ✍️ writer | 写作者 | 文档、报告、文案、翻译 |
| 🎨 designer | 设计师 | 配图、插画、数据可视化 |
| 📊 analyst | 分析师 | 数据处理、统计分析、趋势预测 |
| 🔎 reviewer | 审核员 | 代码审查、内容审核、合规检查 |
| 💬 assistant | 助手 | 简单问答、消息转发、提醒 |
| 🤖 automator | 自动化 | 定时任务、网页自动化、脚本 |
| 🔥 github-tracker | GitHub追踪 | 热门项目追踪、趋势分析 |

## 🚀 快速开始

### 1. 安装技能

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://gitlab.chehejia.com/lidapeng3/openclaw-swarm.git agent-swarm
```

### 2. 配置向导

首次使用时运行配置向导：

```bash
python3 agent-swarm/scripts/setup_wizard.py
```

向导会：
- 检测你的 OpenClaw 已配置的模型
- 建议智能体与模型的最优分配
- 生成配置补丁文件

### 3. 应用配置

将生成的配置补丁应用到 OpenClaw：

```bash
# 使用 gateway 工具应用配置
gateway config.patch --file agent-swarm/config-patch.json
```

### 4. 开始使用

在对话中直接描述复杂任务，Agent Swarm 会自动编排：

```
用户: 帮我调研主流 AI Agent 框架，写一篇对比分析文章

Agent Swarm 编排:
├── 🔍 researcher × 3 (并行调研 LangChain/AutoGPT/CrewAI)
├── ✍️ writer (整合资料，撰写文章)
├── 🎨 designer (生成对比图表)
└── 🔎 reviewer (审核质量)
```

## 📖 使用示例

### 技术调研报告

```
调研 xxx 技术，写一篇深度分析报告
```

### 代码项目重构

```
帮我重构这个项目的认证模块
```

### 数据分析报告

```
分析这份销售数据，生成月度报告
```

### 自动化任务

```
帮我设置每天早上自动检查 GitHub trending
```

## 🛠️ 脚本工具

| 脚本 | 功能 |
|------|------|
| `setup_wizard.py` | 配置向导，检测模型并生成配置 |
| `agent_manager.py` | 智能体管理（增删改查） |
| `init_agents.py` | 初始化智能体工作目录 |
| `experience_logger.py` | 智能体经验记录管理 |

## 📁 目录结构

```
agent-swarm/
├── SKILL.md              # 主技能文档（必读）
├── README.md             # 项目说明（本文件）
├── scripts/
│   ├── setup_wizard.py   # 配置向导
│   ├── agent_manager.py  # 智能体管理
│   ├── init_agents.py    # 初始化脚本
│   └── experience_logger.py
└── references/
    ├── setup-guide.md    # 详细部署指南
    └── statistics-template.md
```

## 🔧 自定义配置

### 添加新智能体

```bash
python3 scripts/agent_manager.py add my_agent \
  --template researcher \
  --name "我的智能体" \
  --emoji "🚀"
```

### 修改模型分配

编辑 `config-patch.json` 中的 `model.primary` 字段。

## 📊 成本优化建议

| 任务类型 | 推荐模型等级 | 示例模型 |
|----------|-------------|----------|
| 复杂编码/分析 | 高性能 | Claude Opus, GPT-4o |
| 文档写作/规划 | 中等 | Gemini Pro, Claude Sonnet |
| 信息搜集/问答 | 轻量 | GLM-4, DeepSeek |

## 🤝 贡献

欢迎提交 Issue 和 Merge Request！

## 📄 许可证

MIT License

---

<p align="center">
  Made with ❤️ for <a href="https://github.com/anthropics/claude-code">OpenClaw</a>
</p>
