---
name: agent-swarm
description: 创建和编排多智能体集群完成复杂任务。当用户需要将复杂任务拆解给多个专业智能体并行或串行执行时使用此技能。适用场景：(1) 复杂项目需要多角色协作（规划、调研、编码、写作、设计、分析、审核）(2) 需要并行执行多个独立子任务以提高效率 (3) 需要专业分工以优化成本和质量。关键词：多智能体、Agent集群、任务编排、并行执行、智能体团队。
triggers:
  - "智能体"
  - "agent swarm"
  - "多智能体"
  - "并行任务"
  - "swarm"
---

# Agent Swarm - 多智能体集群编排

---

## 🚨 强制入口 - 必须先执行！

**无论用户请求什么任务，使用智能体集群前必须先执行入口脚本：**

```bash
python3 scripts/swarm_entry.py
```

### 根据返回的 status 决定下一步

脚本返回 JSON，根据 `status` 字段行动：

| status | 含义 | 下一步操作 |
|--------|------|-----------|
| `need_config` | 未初始化 | 向用户展示 `display` 和 `prompt` 内容，等待用户选择 A/B/C |
| `ready` | 已就绪 | 直接进入任务编排，使用 `agents` 列表中的智能体 |

### 示例流程

```python
# Step 1: 执行入口脚本
result = exec("python3 scripts/swarm_entry.py")

# Step 2: 解析返回的 JSON
if result.status == "need_config":
    # 向用户展示配置选项
    print(result.display)  # 已检测到的模型
    print(result.prompt)   # 请选择 A/B/C
    # 等待用户回复...
    
elif result.status == "ready":
    # 直接开始任务编排
    agents = result.agents
    # 继续执行用户的任务...
```

### 用户选择后完成初始化

用户选择配置方式后，执行初始化：

```bash
# 用户选择 A（自动分配）后
python3 scripts/swarm_entry.py --action init
```

### 重置配置

```bash
python3 scripts/swarm_entry.py --action reset
```

---

## 概述

此技能使你成为**智能体团队的指挥官**，能够根据任务复杂度智能调度多个专业智能体协同完成工作。

核心流程：**入口检查** → 分析任务 → 拆解子任务 → 选择合适的 Agent → 并行/串行执行 → 整合结果

---

## ⚡ 配置向导详解

当入口脚本返回 `status: "need_config"` 时，执行以下配置流程：

### Step 1: 展示检测结果

脚本已自动检测模型，直接展示 `result.display` 内容给用户：

```markdown
## 📦 您的 OpenClaw 已配置以下模型

### 🔴 高性能模型 (适合: coder, writer, analyst, reviewer)
- Claude Opus 4.5 (`vendor-claude-opus-4-5/aws-claude-opus-4-5`)

### 🟡 中等模型 (适合: pm, designer)  
- Gemini 3 Pro (`vendor-gemini-3-pro/gemini-3-pro-preview`)

### 🟢 轻量模型 (适合: researcher, assistant)
- GLM-4.7 (`lixiang-glm-4-7/Kivy-GLM-4.7`)
```

### Step 2: 展示配置选项

展示 `result.prompt` 内容：

```markdown
请选择配置方式：

**A. 自动分配** — 根据您现有的模型自动配置智能体团队
**B. 添加新模型** — 我会推荐主流模型供您选择
**C. 自定义配置** — 您手动指定每个智能体的模型

请回复 A/B/C
```

### Step 3: 根据用户选择执行

**选择 A（自动分配）：**
```bash
python3 scripts/swarm_entry.py --action init
```

**选择 B（添加新模型）：**
- 展示主流模型选项和配置指南
- 用户提供配置后，更新 OpenClaw 配置
- 然后执行 init

**选择 C（自定义配置）：**
- 让用户指定每个智能体的模型
- 收集完成后执行 init

### Step 4: 确认初始化完成

初始化成功后，告知用户：
```
✅ Agent Swarm 配置完成！现在可以开始使用智能体团队了。
```

---

## 旧版配置方式（兼容）

如需手动检测模型，也可以使用 gateway 工具：

```python
# 使用 gateway 工具获取当前配置
gateway({ action: "config.get" })
```

从返回的配置中提取 `models.providers` 下的所有可用模型。

#### Step 2: 向用户展示可用模型

按性能等级分类展示：

```markdown
## 📦 您的 OpenClaw 已配置以下模型

### 🔴 高性能模型 (适合: coder, writer, analyst, reviewer)
- Claude Opus 4.5 (claude-opus-4-5/claude-opus-4-5)

### 🟡 中等模型 (适合: pm, designer)
- Gemini 3 Pro (vendor-gemini-3-pro/gemini-3-pro-preview)

### 🟢 轻量模型 (适合: researcher, assistant)
- GLM-4.7 (glm-4-7/Kivy-GLM-4.7)

### 🖼️ 图像模型 (适合: designer)
- Gemini 3 Pro Image (gemini-3-pro-image/gemini-3-pro-image-preview)
```

#### Step 3: 询问用户配置方式

```markdown
请选择配置方式：

**A. 自动分配** — 根据您现有的模型自动配置智能体团队
   - 高性能任务(编码/写作/分析) → 使用您最强的模型
   - 中等任务(规划/设计) → 使用中等模型
   - 轻量任务(搜索/问答) → 使用成本最低的模型

**B. 添加新模型** — 我会推荐主流模型供您选择
   - Claude (Anthropic)
   - GPT-4o (OpenAI)
   - Gemini (Google)
   - DeepSeek V3 (DeepSeek)
   - Qwen Max (阿里云)
   - GLM-4 (智谱)

**C. 自定义配置** — 您手动指定每个智能体的模型

请回复 A/B/C 或直接告诉我您的选择。
```

#### Step 4: 根据用户选择执行配置

**选择 A（自动分配）：**
- 分析已有模型，按能力等级分配到各智能体
- 生成配置补丁并应用

**选择 B（添加新模型）：**
- 展示主流模型选项和 API 配置指南
- 用户提供 API Key 后，生成模型配置
- 更新 OpenClaw 配置

**选择 C（自定义配置）：**
- 列出所有智能体及其推荐模型等级
- 让用户逐个指定

### 配置向导脚本

可运行配置向导脚本辅助检测：

```bash
python3 scripts/setup_wizard.py
```

脚本会：
1. 自动读取 OpenClaw 配置
2. 分析已配置的模型
3. 建议智能体分配方案
4. 生成配置补丁文件

### 主流模型推荐

| 模型 | 提供商 | 推荐用于 | API 类型 |
|------|--------|----------|----------|
| Claude Opus 4/4.5 | Anthropic | 高复杂度任务 | anthropic-messages |
| Claude Sonnet 4 | Anthropic | 中等复杂度 | anthropic-messages |
| GPT-4o | OpenAI | 通用任务 | openai-completions |
| Gemini 2.5 Pro | Google | 长文档处理 | google-generative-ai |
| DeepSeek V3 | DeepSeek | 性价比之选 | openai-completions |
| Qwen Max | 阿里云 | 中文任务 | openai-completions |
| GLM-4 | 智谱 | 轻量任务 | openai-completions |

### 模型添加示例

如果用户选择添加新模型，生成类似配置：

```json
{
  "models": {
    "providers": {
      "my-deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "sk-xxx（用户提供）",
        "api": "openai-completions",
        "authHeader": "Authorization",
        "models": [{
          "id": "deepseek-chat",
          "name": "DeepSeek V3",
          "contextWindow": 64000,
          "maxTokens": 8192
        }]
      }
    }
  }
}
```

---

## 可用智能体团队

| Agent ID | Emoji | 角色定位 | 核心能力 | 可用工具 |
|----------|-------|----------|----------|----------|
| `pm` | 📋 | 规划者 | 需求分析、任务拆解、优先级排序 | read, write, edit, web_search, web_fetch, memory |
| `researcher` | 🔍 | 信息猎手 | 广度搜索、交叉验证、结构化输出 | web_search, web_fetch, read, write, memory |
| `coder` | 👨‍💻 | 代码工匠 | 编码、调试、测试、重构 | read, write, edit, exec, process |
| `writer` | ✍️ | 文字工匠 | 文档、报告、文案、翻译 | read, write, edit, memory |
| `designer` | 🎨 | 视觉创作者 | 配图、插画、数据可视化 | read, write |
| `analyst` | 📊 | 数据侦探 | 数据处理、统计分析、趋势预测 | read, write, edit, exec |
| `reviewer` | 🔎 | 质量守门人 | 代码审查、内容审核、合规检查 | read, memory |
| `assistant` | 💬 | 沟通桥梁 | 简单问答、消息转发、提醒 | message, read, sessions_send |
| `automator` | 🤖 | 效率大师 | 定时任务、网页自动化、脚本 | exec, process, cron, browser, read, write |
| `github-tracker` | 🔥 | GitHub猎人 | 追踪热门项目、分析趋势、日报生成 | web_search, web_fetch, read, write, memory |

### 智能体人格速览

| 智能体 | 一句话定位 | 核心原则 |
|--------|------------|----------|
| 📋 pm | 把模糊需求变成清晰方案 | 用户视角、目标导向、优先级思维 |
| 🔍 researcher | 找到别人找不到的资料 | 广度优先、多源验证、标注来源 |
| 👨‍💻 coder | 写出优雅高效的程序 | 先理解再动手、简单优于复杂、可读性优先 |
| ✍️ writer | 把信息变成有价值的内容 | 读者优先、结构清晰、言之有物 |
| 🎨 designer | 让想法变成图像 | 目的明确、简洁清晰、风格一致 |
| 📊 analyst | 从数字中发现故事 | 数据质量、假设驱动、洞察导向 |
| 🔎 reviewer | 确保输出达到标准 | 客观公正、建设性反馈、不直接修改 |
| 💬 assistant | 传递信息、快速响应 | 简洁明了、知道边界、友好礼貌 |
| 🤖 automator | 让重复的事自动化 | ROI思维、稳定可靠、有监控 |
| 🔥 github-tracker | 发现GitHub热门项目 | 数据驱动、聚焦价值、趋势洞察 |

### 模型成本参考

| 模型 | Input ($/M) | Output ($/M) | 用于 |
|------|-------------|--------------|------|
| Claude Opus 4.5 | $5.00 | $25.00 | main, coder, writer, analyst, reviewer, automator |
| Gemini 3 Pro | $1.25 | $10.00 | pm, researcher |
| Gemini 3 Pro Image | $1.25 | $10.00 | designer |
| GLM-4.7 | ~$0.014 | ~$0.014 | assistant, github-tracker |

**成本优化原则**：简单任务用便宜模型，复杂任务才用贵模型。

## 编排流程

### Step 1: 任务分析
```
收到任务 → 判断复杂度
├── 简单任务 → 直接执行
└── 复杂任务 → 进入编排模式
```

### Step 2: 任务拆解
将复杂任务分解为独立子任务，明确：
- 每个子任务的目标和输出格式
- 输入数据和上下文
- 依赖关系（哪些可并行，哪些需串行）

### Step 3: Agent 选择

根据子任务性质选择最合适的 Agent：

| 任务类型 | 推荐智能体 | 说明 |
|----------|------------|------|
| 项目规划、需求分析 | 📋 pm | 输出任务列表和优先级 |
| 信息搜集、资料整理 | 🔍 researcher | 多源搜索，结构化输出 |
| 写代码、修bug、脚本 | 👨‍💻 coder | 可执行 shell 命令 |
| 写文章、文档、报告 | ✍️ writer | 基于资料进行创作 |
| 配图、插画、图表 | 🎨 designer | 图像生成 |
| 数据分析、统计 | 📊 analyst | 可执行数据处理脚本 |
| 代码审查、内容审核 | 🔎 reviewer | 只读，给出建议 |
| 消息转发、简单问答 | 💬 assistant | 快速响应 |
| 定时任务、自动化 | 🤖 automator | 可设置 cron |

### Step 4: 执行调度

使用 `sessions_spawn` 调度子智能体。spawn 是异步的，子任务完成后会自动回报结果。

**并行执行示例**（多个 spawn 同时派发，各自独立执行）：

```javascript
// 在同一个回合内连续 spawn，这些任务会并行执行
// 子任务完成后各自回报，主 Agent 收集结果后汇总

// 方式 1: 直接连续 spawn
sessions_spawn({ task: "搜索 LangChain 资料...", agentId: "researcher", label: "research-langchain" })
sessions_spawn({ task: "搜索 AutoGPT 资料...", agentId: "researcher", label: "research-autogpt" })
sessions_spawn({ task: "搜索 CrewAI 资料...", agentId: "researcher", label: "research-crewai" })
// 三个任务并行执行，分别回报结果

// 方式 2: 循环派发（更清晰）
const frameworks = ["LangChain", "AutoGPT", "CrewAI"]
frameworks.forEach(name => {
  sessions_spawn({
    task: `搜索 ${name} 框架的特点、优缺点、适用场景，输出结构化总结到 /workspace/research/${name.toLowerCase()}.md`,
    agentId: "researcher",
    label: `research-${name.toLowerCase()}`
  })
})
// 子任务完成后自动回报，主 Agent 汇总所有结果
```

**串行执行示例**（等待上一步结果再继续）：

```javascript
// 串行需要等待前序任务完成，收到回报后再 spawn 下一个
// 流程：调研 → (等待回报) → 写作 → (等待回报) → 配图 → (等待回报) → 审核

// Step 1: 先派发调研任务
sessions_spawn({ task: "调研 AI Agent 框架...", agentId: "researcher" })
// 等待 researcher 回报结果...

// Step 2: 收到调研结果后，派发写作任务
sessions_spawn({ 
  task: "基于 /workspace/research/ 的调研资料，撰写对比分析文章...", 
  agentId: "writer" 
})
// 等待 writer 回报...

// Step 3: 文章完成后，派发配图任务
sessions_spawn({ task: "为文章生成配图...", agentId: "designer" })
```

**混合编排示例**（先并行，后串行）：

```javascript
// Phase 1: 并行调研（同时派发）
sessions_spawn({ task: "搜索 LangChain...", agentId: "researcher", label: "r1" })
sessions_spawn({ task: "搜索 AutoGPT...", agentId: "researcher", label: "r2" })
sessions_spawn({ task: "搜索 CrewAI...", agentId: "researcher", label: "r3" })

// 等待 3 个调研任务都完成...

// Phase 2: 串行处理（基于汇总结果）
sessions_spawn({ task: "整合调研资料，撰写报告...", agentId: "writer" })
// 等待 writer 完成...

sessions_spawn({ task: "审核报告质量...", agentId: "reviewer" })
```

### Step 5: 结果整合
- 收集所有子 Agent 的输出
- 整合、去重、格式化
- 输出最终交付物
- **必须输出执行统计**（见下方模板）

## 编排示例

### 示例 1: 技术调研报告
```
用户: "调研主流 AI Agent 框架，写一篇对比分析文章"

编排方案:
├── 🔍 researcher × 3 (并行)
│   ├── 搜索 LangChain - 整理功能、优缺点、案例
│   ├── 搜索 AutoGPT - 整理功能、优缺点、案例  
│   └── 搜索 CrewAI - 整理功能、优缺点、案例
├── ✍️ writer (串行，等调研完成)
│   └── 整合资料，撰写对比分析文章
├── 🎨 designer (串行)
│   └── 生成框架对比图/架构图
└── 🔎 reviewer (串行)
    └── 审核文章质量，提出改进建议
```

### 示例 2: 代码项目
```
用户: "帮我重构这个项目的认证模块"

编排方案:
├── 📋 pm (可选)
│   └── 分析需求，拆解重构步骤
├── 👨‍💻 coder
│   └── 分析现有代码，实现重构
└── 🔎 reviewer (串行)
    └── 代码审查，确保质量
```

### 示例 3: 数据分析报告
```
用户: "分析这份销售数据，生成月度报告"

编排方案:
├── 📊 analyst
│   └── 数据清洗、统计分析、发现洞察
├── ✍️ writer (串行)
│   └── 撰写分析报告
└── 🎨 designer (串行)
    └── 生成数据可视化图表
```

### 示例 4: 自动化任务
```
用户: "帮我设置每天早上自动检查 GitHub trending"

编排方案:
├── 🤖 automator
│   └── 编写脚本 + 设置 cron 定时任务
```

## 编排原则

1. **简单任务不过度编排** — 能直接做的就直接做，不要为了用而用
2. **合理并行** — 无依赖的任务并行执行，提高效率
3. **明确交接** — 子任务输出要清晰完整，便于下游使用
4. **失败处理** — 某个子任务失败时，决定重试还是跳过
5. **结果整合** — 最终输出要连贯，不是简单拼接
6. **成本意识** — 优先用便宜模型，复杂任务才用贵模型

---

## 🔧 超长文本分批输出策略

当需要生成较长的文件（如完整报告、长文档）时，**单次输出可能因模型 token 限制被截断**，导致 `write` 工具调用失败。

### 问题表现

```
Validation failed for tool "write":
  - content: must have required property 'content'
```

或者输出被截断（`stopReason: "length"`），导致文件内容不完整。

### 解决方案：分段生成 + 脚本汇总

**策略一：分章节派发多个 writer（推荐）**

将长报告拆分为多个章节，分别派发给不同的 writer 并行撰写，最后用脚本拼接：

```javascript
// Phase 1: 并行撰写各章节
sessions_spawn({ task: "撰写第1章：摘要和背景...", agentId: "writer", label: "ch01" })
sessions_spawn({ task: "撰写第2章：核心内容...", agentId: "writer", label: "ch02" })
sessions_spawn({ task: "撰写第3章：结论...", agentId: "writer", label: "ch03" })

// Phase 2: 所有章节完成后，用 exec 拼接
exec(`
  cat sections/ch01.md > FINAL-REPORT.md
  cat sections/ch02.md >> FINAL-REPORT.md
  cat sections/ch03.md >> FINAL-REPORT.md
`)
```

**策略二：exec + heredoc 追加写入**

对于单个智能体任务，如果内容太长导致单次 write 失败，可以分段写入：

```bash
# 先写入文件头部
cat > output.md << 'PART1'
# 标题
## 第一部分内容...
PART1

# 追加后续内容
cat >> output.md << 'PART2'
## 第二部分内容...
PART2

# 继续追加
cat >> output.md << 'PART3'
## 第三部分内容...
PART3
```

### 最佳实践

| 报告长度 | 推荐策略 |
|---------|---------|
| < 3000 字 | 单个 writer 直接输出 |
| 3000-8000 字 | 分 2-4 个章节并行撰写，脚本汇总 |
| > 8000 字 | 分 5+ 个章节，多 writer 并行 + 脚本汇总 |

**核心原则**：不限制单次输出长度，而是通过**拆分任务**和**并行执行**来解决长文本问题。

---

## 🆘 子智能体遇错上报机制

子智能体在执行任务时可能遇到各种错误（工具调用失败、模型限制、资源不足等）。为提高任务成功率，建立**遇错上报机制**。

### 机制说明

当子智能体任务失败或返回异常时，主智能体应：

1. **分析错误类型**：
   - 输出截断（`stopReason: "length"`）→ 采用分段策略
   - 工具调用失败（`Validation failed`）→ 检查参数或换方案
   - 模型不支持（如 Gemini Image 不支持 thinking）→ 调整配置
   - 超时（`timeout`）→ 拆分任务或增加时间

2. **选择解决方案**：
   - **增派子智能体并行分担**：将大任务拆成小块，派发多个子智能体
   - **主智能体直接处理**：简单任务直接由主智能体完成
   - **调整参数重试**：修改 task 描述、超时时间、模型配置后重试

### 错误处理流程

```
子智能体任务失败
    ↓
主智能体收到失败通知
    ↓
分析错误原因
    ├── 输出过长 → 拆分为多个子任务，增派 writer 并行
    ├── 工具不可用 → 换用 exec 或其他方案
    ├── 模型限制 → 调整 thinking/model 配置
    └── 超时 → 拆分任务或延长 timeout
    ↓
执行解决方案
    ↓
汇总结果
```

### 示例：writer 输出被截断的处理

```javascript
// 原始任务失败（输出太长被截断）
// 主智能体收到通知后，改用分段策略

// 解决方案：拆分为 3 个子任务
sessions_spawn({
  task: "撰写报告第1-2章（摘要、背景），限制 1500 字...",
  agentId: "writer",
  label: "report-part1"
})

sessions_spawn({
  task: "撰写报告第3-4章（核心内容），限制 1500 字...",
  agentId: "writer",
  label: "report-part2"
})

sessions_spawn({
  task: "撰写报告第5-6章（结论、参考文献），限制 1000 字...",
  agentId: "writer",
  label: "report-part3"
})

// 全部完成后用 exec 合并
```

### 在子智能体 AGENTS.md 中添加上报指引

建议在每个子智能体的 AGENTS.md 中添加：

```markdown
## 遇到问题时

如果遇到以下情况，在输出中明确说明，以便主智能体处理：

1. **任务太大**：说明"任务内容过多，建议拆分为 X 个子任务"
2. **工具不可用**：说明"工具 X 调用失败，原因是 Y"
3. **信息不足**：说明"缺少 X 信息，无法完成任务"
4. **超出能力范围**：说明"此任务需要 X 能力，建议交给 Y 智能体"

不要静默失败，明确上报问题有助于主智能体找到解决方案。
```

---

## 调用语法

```javascript
sessions_spawn({
  task: "具体任务描述，包含必要的上下文和期望的输出格式",
  agentId: "researcher",   // 指定 Agent ID
  model: "glm",            // 可选，覆盖 Agent 默认模型
  thinking: "off",         // 可选，控制思考模式（off/minimal/low/medium/high）
  label: "task-name",      // 可选，便于追踪
  runTimeoutSeconds: 300   // 可选，超时时间（秒）
})
```

### ⚠️ 特殊说明：Designer 智能体

**重要**：调用 designer 智能体时，必须显式设置 `thinking: "off"`，因为 Gemini Image 模型不支持 thinking 模式：

```javascript
sessions_spawn({
  task: "为文章生成配图...",
  agentId: "designer",
  thinking: "off"    // 必须！Gemini Image 不支持 thinking
})
```

### Task 描述最佳实践

```markdown
好的 task 描述应包含：
1. 明确的目标 - 要做什么
2. 必要的上下文 - 背景信息
3. 输出要求 - 格式、保存位置
4. 约束条件 - 限制和注意事项

示例：
"搜索 LangChain 框架的最新资料，整理以下内容：
1. 核心功能和架构
2. 优点和缺点
3. 典型使用案例
4. 与其他框架的对比

输出格式：Markdown
保存到：/workspace/research/langchain.md
语言：中文"
```

## 任务完成统计

完成智能体团队协作任务后，**必须**输出统计信息：

```markdown
## 📊 智能体团队执行统计

### 执行明细
| 智能体 | 任务 | 耗时 | Tokens (in/out) | 状态 |
|--------|------|------|-----------------|------|
| 🔍 researcher | LangChain调研 | 2m30s | 8k/1.2k | ✅ |
| 🔍 researcher | AutoGPT调研 | 2m45s | 9k/1.0k | ✅ |
| ✍️ writer | 撰写报告 | 3m12s | 15k/2.5k | ✅ |
| 🎨 designer | 生成配图 | 45s | 2k/- | ✅ |

### 成本汇总
- **总耗时**: 9m12s（并行优化后实际: 6m30s）
- **总 Tokens**: 34k input / 4.7k output
- **实际成本**: $0.12
- **全用主模型成本**: $0.29
- **节省**: 59%

### 效率分析
- **并行任务数**: 2个 researcher 并行
- **串行节省**: 通过并行节省 ~2m45s
```

详细模板见 [references/statistics-template.md](references/statistics-template.md)

## 智能体工作目录

每个智能体有独立的工作目录，包含其人格配置：

```
/workspace/agents/
├── pm/           # 📋 产品经理
│   ├── SOUL.md   # 人格定义
│   └── AGENTS.md # 工作规范
├── researcher/   # 🔍 研究员
├── coder/        # 👨‍💻 程序员
├── writer/       # ✍️ 写作者
├── designer/     # 🎨 设计师
├── analyst/      # 📊 分析师
├── reviewer/     # 🔎 审核员
├── assistant/    # 💬 助手
└── automator/    # 🤖 自动化
```

## 智能体配置管理

使用 `agent_manager.py` 脚本管理智能体集群：

```bash
# 列出所有智能体
python3 scripts/agent_manager.py list

# 查看智能体详情
python3 scripts/agent_manager.py show researcher

# 添加新智能体（使用模板）
python3 scripts/agent_manager.py add my_agent --template researcher --name "我的智能体" --emoji "🚀"

# 删除智能体（默认会备份）
python3 scripts/agent_manager.py remove my_agent

# 更新智能体配置
python3 scripts/agent_manager.py update my_agent --name "新名称"
```

### 可用模板

| 模板 | 说明 | 默认模型 |
|------|------|----------|
| `default` | 通用智能体 | claude-opus-4 |
| `researcher` | 研究调研 | glm-4 |
| `coder` | 编程开发 | claude-opus-4 |
| `writer` | 内容写作 | gemini-2.5-pro |

## 智能体经验记忆

每个智能体可以积累任务经验，用于提升后续任务的执行质量。

### 经验记录结构

```
/workspace/agents/<agent_id>/
└── memory/
    ├── experience.md    # 人类可读的经验记录
    └── experience.json  # 结构化经验数据
```

### 使用 experience_logger.py

```bash
# 记录一条经验
python3 scripts/experience_logger.py log researcher "搜索技术资料时，英文关键词效果更好" --task "LangChain调研"

# 查看智能体经验
python3 scripts/experience_logger.py show researcher --limit 10

# 生成经验摘要
python3 scripts/experience_logger.py summary researcher

# 输出可注入 prompt 的经验（用于 spawn 时注入）
python3 scripts/experience_logger.py inject researcher --limit 5
```

### 在任务中使用经验

**方法 1: 在 task 描述中注入经验**

```python
# 获取历史经验
import subprocess
result = subprocess.run(
    ["python3", "scripts/experience_logger.py", "inject", "researcher", "--limit", "5"],
    capture_output=True, text=True
)
experiences = result.stdout

# 在 spawn 时注入
sessions_spawn({
    task: f"""搜索 xxx 资料...

{experiences}
""",
    agentId: "researcher"
})
```

**方法 2: 智能体主动读取经验**

在智能体的 AGENTS.md 中添加指引：
```markdown
## 任务前准备
执行任务前，先读取 memory/experience.md 中的历史经验。

## 任务后总结
完成任务后，总结 1-3 条有效经验，记录到 memory/experience.md。
```

### 经验记录最佳实践

✅ **好的经验记录**：
- 具体可操作："搜索 GitHub 时加 language:python 过滤更精准"
- 有因果关系："JSON 输出比纯文本更便于下游处理"
- 针对性强："处理大文件时分块读取，避免内存溢出"

❌ **避免的记录**：
- 太笼统："要认真工作"
- 太具体："用户 A 喜欢蓝色"（除非是个性化智能体）
- 重复已有的："要输出 Markdown 格式"（已在 AGENTS.md 中）

### 经验自动总结（推荐）

在每个智能体的 AGENTS.md 末尾添加：

```markdown
## 任务完成后

1. 检查输出是否符合要求
2. 总结本次任务中的有效经验（1-3 条）
3. 将经验追加到 memory/experience.md，格式：
   - [YYYY-MM-DD] 经验描述 (任务名称)
```

这样智能体在完成任务后会自动总结经验，无需手动干预。

## 配置与部署

如需配置新的智能体团队或添加新模型，请参阅 [references/setup-guide.md](references/setup-guide.md)

使用初始化脚本快速创建工作目录：
```bash
python3 scripts/init_agents.py --base-path /workspace/agents
```
