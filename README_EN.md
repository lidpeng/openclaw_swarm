<p align="center">
  <img src="pic/openclaw-swarm-en.png" alt="OpenClaw Swarm Promotional Image" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Swarm-blue?style=for-the-badge" alt="OpenClaw Swarm"/>
  <img src="https://img.shields.io/badge/version-1.0.0-green?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/license-MIT-orange?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🐝 OpenClaw Swarm</h1>

<p align="center">
  <strong>Upgrade your OpenClaw from "solo fight 🦞" to "team battle 🦞🦞🦞"!</strong>
</p>

<p align="center">
  <strong>Work from Li Auto Inc.</strong>
</p>
<p align="center">
  <strong>The first agent swarm implemented based on Openclaw</strong>
</p>
<p align="center">
  <a href="README.md">🇨🇳 中文</a> | <a href="README_EN.md">🇺🇸 English</a>
</p>

---

## 🎬 Live Demo Showcase

<p align="center">
  <strong>See OpenClaw Swarm in Action</strong>
</p>

<table align="center">
  <tr>
    <td align="center" width="50%">
      <h3>🔬 Reinforcement Learning Research</h3>
      <p>Multi-agent parallel research generating comprehensive technical analysis report and development roadmap</p>
      <p>
        <a href="https://lidpeng.github.io/rl_case_visualization/" target="_blank">
          <img src="https://img.shields.io/badge/🚀_Live_Demo-RL_Case-brightgreen?style=for-the-badge" alt="RL Case Demo"/>
        </a>
      </p>
      <p><em>Agents involved: 🔍 researcher × 3, ✍️ writer × n, 🎨 designer</em></p>
    </td>
    <td align="center" width="50%">
      <h3>📊 Silver Price Market Analysis</h3>
      <p>Multi-perspective market research generating in-depth analysis article and interactive visualization webpage</p>
      <p>
        <a href="https://lidpeng.github.io/silver_case_visualization/" target="_blank">
          <img src="https://img.shields.io/badge/🚀_Live_Demo-Silver_Case-blue?style=for-the-badge" alt="Silver Case Demo"/>
        </a>
      </p>
      <p><em>Agents involved: 🔍 researcher × 3, ✍️ writer, 🔎 reviewer, 👨‍💻 coder</em></p>
    </td>
  </tr>
</table>

<p align="center">
  <em>💡 These two cases demonstrate how OpenClaw Swarm efficiently completes complex tasks through multi-agent parallel collaboration</em>
</p>

---

## 📖 Project Introduction

OpenClaw is highly effective for handling simple and automated tasks, but faces several pain points when dealing with complex tasks:

| Issue | Description |
|-------|-------------|
| ⏱️ **Extremely Time-Consuming** | Default linear serial execution makes ultra-long tasks extremely time-consuming |
| 📄 **Poor Robustness** | Single task errors in long task chains may cause overall failure, with opaque intermediate processes |
| 🔥 **Very Expensive** | Using Opus 4.5 model by default, complex daily tasks can burn hundreds of dollars |

**OpenClaw Swarm Solution:**

Decompose complex tasks into multiple subtasks, assign appropriate sub-agents to complete them **in parallel**, using powerful models for high-difficulty tasks and cheap models for simple tasks.

> 💡 **One-sentence Summary**: Transform OpenClaw from "working alone" to "leading a team". Like a project manager in a company, instead of doing everything from start to finish alone when receiving complex tasks, break down tasks into smaller pieces and assign them to different professionals (researchers gather information, programmers write code, designers create graphics), everyone works in parallel, and finally consolidate results.

## ✨ Core Advantages

| Capability | Description |
|------------|-------------|
| 🔀 **Parallel Tasks** | Multiple independent subtasks execute simultaneously, no more queuing |
| 💰 **Cost Optimization** | Use cheap models (GLM) for simple tasks, expensive models (Claude) only for complex tasks, **tested to save 50-70% cost** |
| 🔧 **Fully Customizable** | Each agent has an independent personality file (SOUL.md), can add/delete/modify anytime, fine-grained tool permission control |
| 📚 **Experience Accumulation** | Agents record effective experiences, automatically injected when executing similar tasks next time, getting smarter with use, not starting from zero each time |
| 🏠 **Local First** | Runs entirely on your own OpenClaw instance, data doesn't pass through third parties, can work offline |

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

> 💡 Currently implemented as static multi-agent cluster, we'll also try dynamically generating team configurations in the future

## 🚀 Quick Start - Installation Instructions

Give the URL of this repository to OpenClaw and let it install automatically.

### Post-Installation Verification

```bash
# 1. Check agent team
openclaw agents list

# 2. Restart conversation
/new

# 3. Restart gateway
openclaw gateway restart
```

## 📚 Use Cases

### Case 1: 🔬 Technical Research Report

> "Research reinforcement learning technology and write an analysis report. Search from Arxiv, GitHub, web channels, and various tutorials to gather information, generate a complete document, and finally generate a roadmap to show the complete development context of agent reinforcement learning. Generate the report in batches and finally consolidate."

**Execution Flow:**
```
├── 🔍 researcher × 3 (parallel)
│   ├── Search Arxiv papers
│   ├── Search GitHub projects
│   └── Search web resources
├── ✍️ writer x n (parallel)
│   └── Consolidate materials, write analysis report
└── 🎨 designer (serial)
    └── Generate technology development roadmap
```

**🎬 [View Live Demo →](https://lidpeng.github.io/rl_case_visualization/)**

---

### Case 2: 📊 Market Research & Web Visualization

> "Now use multi-agent capabilities to help me complete the following task: I want to write an article about how long silver prices can continue to rise. Research and debate from different perspectives including objective data, bullish views, and bearish views. Then have one agent specifically responsible for writing. Another person will review the manuscript and verify content authenticity. Finally, have a developer present the data and article content in an interactive webpage format."

**Execution Flow:**
```
├── 🔍 researcher × 3 (parallel)
│   ├── Objective data research
│   ├── Bullish views collection
│   └── Bearish views collection
├── ✍️ writer → 🔎 reviewer (serial)
└── 👨‍💻 coder (serial)
    └── Develop interactive webpage
```

**🎬 [View Live Demo →](https://lidpeng.github.io/silver_case_visualization/)**

---

### Case 3: 🐙 GitHub Project Research

> "Research mainstream AI Agent frameworks (LangChain, AutoGPT, CrewAI) and perform comparative analysis"

---

### Case 4: 📚 Batch Data Processing

> "Translate all Buffett's letters to shareholders from the last ten years into Chinese: https://www.berkshirehathaway.com/letters/letters.html and create a summary document listing a series of learnable lessons."

**Efficiency Analysis:**
- ⏱️ Time Savings: From serial hours reduced to parallel dozens of minutes
- 💰 Token Cost: Using GLM for simple tasks instead of Claude saves 50-70%

---

### Case 5: 🐱 Image Generation

> "Help me draw four cats in different styles!"

Supports image generation after configuring Gemini image model.

---

### Case 6: 🎬 Animation Storyboard

> "https://paulgraham.com/greatwork.html I want to make this article into a video. Please translate this article into Chinese, then generate 5 storyboard images with unified style, using Pixar style, design one or two fixed characters, and use charts when necessary."

## 🎯 Applicable Scenarios

### ✅ Suitable for Swarm

- **Technical Research Reports** — Multi-framework parallel research
- **Code Projects** — Analysis → Coding → Review
- **Data Analysis Reports** — Processing → Analysis → Visualization → Writing
- **Content Creation** — Research → Writing → Illustration → Review

### ❌ Not Suitable for Swarm

- **Simple Q&A** — Just ask directly
- **Single Task** — No need to break down
- **Real-time Conversation** — High latency requirements

## 🔧 Advanced Configuration

### 🎨 Customized Agents

Add customized sub-agents according to needs by conversing with OpenClaw, or modify agent configuration by calling skills.

Example conversation:
> "Help me add a sub-agent to agent swarm, specifically for detecting the latest GitHub trending projects every day"

### 🖼️ Image Generation Model Configuration

After applying for Gemini API, configure in `openclaw.json`:

```json
{
  "vendor-gemini-3-pro-image": {
    "baseUrl": "baseUrl",
    "apiKey": "Your API Key",
    "api": "google-generative-ai",
    "authHeader": "x-goog-api-key",
    "models": [
      {
        "id": "gemini-3-pro-image-preview",
        "name": "Gemini 3 Pro Image",
        "reasoning": false,
        "input": ["text", "image"],
        "cost": { "input": 0, "output": 0 },
        "contextWindow": 1000000,
        "maxTokens": 65536
      }
    ]
  }
}
```

After configuration, test with: `Help me generate an image of a kitten`

## 🛠️ Script Tools

| Script | Function |
|--------|----------|
| `setup_wizard.py` | Configuration wizard, detects models and generates config |
| `agent_manager.py` | Agent management (add/delete/modify/query) |
| `init_agents.py` | Initialize agent working directories |
| `experience_logger.py` | Agent experience record management |

## 🆚 Competitive Comparison

| Feature | OpenClaw Swarm | Kimi K2.5 Swarm | Claude Code Swarm |
|---------|----------------|------------------|-------------------|
| Status | ✅ Available | 🔬 Experimental | 🔬 Experimental |
| Membership Required | None | Highest tier | - |
| Model Selection | ✅ Fully customizable | ❌ Fixed | - |
| Customization | ✅ Highly customizable | ❌ Limited | - |
| Secondary Development | ✅ Low cost | ❌ Not supported | - |

Using OpenClaw provides high customizability, allowing low-barrier yet highly customized secondary development based on your own needs through conversation. Welcome everyone to optimize our skills and provide features.


## 📁 Directory Structure

```
openclaw-swarm/
├── README.md              # Project description (this file)
├── README_EN.md           # English documentation
├── openclaw-swarm/
│   ├── SKILL.md           # Main skill documentation (must read)
│   ├── scripts/
│   │   ├── setup_wizard.py      # Configuration wizard
│   │   ├── agent_manager.py     # Agent management
│   │   ├── init_agents.py       # Initialization script
│   │   ├── config_checker.py    # Configuration checker
│   │   ├── experience_logger.py # Experience logger
│   │   ├── swarm_entry.py       # Entry script
│   │   └── agent_souls.json     # Agent configuration
│   └── references/
│       ├── setup-guide.md       # Detailed deployment guide
│       ├── statistics-template.md # Statistics template
│       └── souls/               # Agent personality files
```

## ⚠️ Declaration
Thanks to the Kimi team, some design ideas and cases of OpenClaw Swarm were inspired by Kimi K2 Swarm.
Currently, the configuration and optimization of OpenClaw Swarm is still in beta stage. This capability may have instability during use, and will be continuously optimized and upgraded in the future, sharing relevant usage experience. Welcome to co-develop & exchange!

## TODO:
- Dynamic agent team configuration generation
- Multi-agent team configuration & task progress visualization

## 📄 License

MIT License

---

<p align="center">
  Made with ❤️ for OpenClaw</a>
</p>
