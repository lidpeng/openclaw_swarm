<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue?style=for-the-badge" alt="OpenClaw Skill"/>
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README_EN.md">🇺🇸 English</a>
</p>

---

# 🤖 Agent Swarm - Multi-Agent Orchestration

> Break down complex tasks for a team of specialized agents working in parallel

## ✨ Features

- 🎯 **10+ Specialized Agents** - PM, Researcher, Coder, Writer, Designer, Analyst, and more
- ⚡ **Parallel Execution** - Run independent tasks simultaneously for maximum efficiency
- 🧠 **Smart Scheduling** - Automatically select the right model based on task complexity
- 💰 **Cost Optimization** - Use cheaper models for simple tasks, powerful models for complex ones
- 📝 **Experience Learning** - Agents can record and reuse historical experiences
- 🔧 **Flexible Configuration** - Support custom agents and model assignments

## 📦 Agent Team

| Agent | Role | Core Capabilities |
|-------|------|-------------------|
| 📋 pm | Product Manager | Requirements analysis, task breakdown, prioritization |
| 🔍 researcher | Researcher | Information gathering, data compilation, multi-source verification |
| 👨‍💻 coder | Programmer | Coding, debugging, testing, refactoring |
| ✍️ writer | Writer | Documentation, reports, copywriting, translation |
| 🎨 designer | Designer | Illustrations, graphics, data visualization |
| 📊 analyst | Analyst | Data processing, statistical analysis, trend forecasting |
| 🔎 reviewer | Reviewer | Code review, content audit, compliance check |
| 💬 assistant | Assistant | Simple Q&A, message forwarding, reminders |
| 🤖 automator | Automator | Scheduled tasks, web automation, scripts |
| 🔥 github-tracker | GitHub Tracker | Trending projects tracking, trend analysis |

## 🚀 Quick Start

### 1. Install the Skill

```bash
# Clone to OpenClaw skills directory
cd ~/.openclaw/skills
git clone https://gitlab.chehejia.com/lidapeng3/openclaw-swarm.git agent-swarm
```

### 2. Run Setup Wizard

Run the setup wizard on first use:

```bash
python3 agent-swarm/scripts/setup_wizard.py
```

The wizard will:
- Detect models configured in your OpenClaw
- Suggest optimal agent-to-model assignments
- Generate a configuration patch file

### 3. Apply Configuration

Apply the generated config patch to OpenClaw:

```bash
# Use gateway tool to apply configuration
gateway config.patch --file agent-swarm/config-patch.json
```

### 4. Start Using

Simply describe complex tasks in conversation, and Agent Swarm will orchestrate automatically:

```
User: Research mainstream AI Agent frameworks and write a comparison article

Agent Swarm Orchestration:
├── 🔍 researcher × 3 (parallel research on LangChain/AutoGPT/CrewAI)
├── ✍️ writer (compile materials, write article)
├── 🎨 designer (create comparison charts)
└── 🔎 reviewer (quality review)
```

## 📖 Usage Examples

### Technical Research Report

```
Research xxx technology and write an in-depth analysis report
```

### Code Project Refactoring

```
Help me refactor the authentication module of this project
```

### Data Analysis Report

```
Analyze this sales data and generate a monthly report
```

### Automation Tasks

```
Set up automatic GitHub trending check every morning
```

## 🛠️ Script Tools

| Script | Function |
|--------|----------|
| `setup_wizard.py` | Setup wizard, detect models and generate config |
| `agent_manager.py` | Agent management (CRUD operations) |
| `init_agents.py` | Initialize agent working directories |
| `experience_logger.py` | Agent experience record management |

## 📁 Directory Structure

```
agent-swarm/
├── SKILL.md              # Main skill documentation (must read)
├── README.md             # Project description (this file)
├── scripts/
│   ├── setup_wizard.py   # Setup wizard
│   ├── agent_manager.py  # Agent management
│   ├── init_agents.py    # Initialization script
│   └── experience_logger.py
└── references/
    ├── setup-guide.md    # Detailed deployment guide
    └── statistics-template.md
```

## 🔧 Custom Configuration

### Add New Agent

```bash
python3 scripts/agent_manager.py add my_agent \
  --template researcher \
  --name "My Agent" \
  --emoji "🚀"
```

### Modify Model Assignment

Edit the `model.primary` field in `config-patch.json`.

## 📊 Cost Optimization Tips

| Task Type | Recommended Model Tier | Example Models |
|-----------|----------------------|----------------|
| Complex coding/analysis | High-performance | Claude Opus, GPT-4o |
| Documentation/planning | Mid-tier | Gemini Pro, Claude Sonnet |
| Information gathering/Q&A | Lightweight | GLM-4, DeepSeek |

## 🤝 Contributing

Issues and Merge Requests are welcome!

## 📄 License

MIT License

---

<p align="center">
  Made with ❤️ for <a href="https://github.com/anthropics/claude-code">OpenClaw</a>
</p>
