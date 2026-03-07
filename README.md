# 每日自动获取AI简讯Agent

🤖 一个基于Python的自动化AI行业资讯采集和生成系统，能够从多个专业数据源自动采集AI新闻，经过智能处理后生成高质量的每日简报。

## ✨ 核心功能

- **全自动定时**: 支持每日8:00和8:30自动触发
- **双重文件机制**: 固定刷新latest.md/index.html + 历史存档
- **智能内容处理**: 11大固定分类 + 优先级算法 + 云厂商视角点评
- **多格式输出**: Markdown、HTML、JSON、Excel
- **增强监控**: 完善的日志系统和数据追踪
- **响应式设计**: 完美适配手机、平板和电脑端
- **一键分享**: 支持分享今日十大精选资讯

## 📋 输入输出规范

### 固定输入
- **数据源配置**: `source/AI_sources.xlsx`
  - 包含24个专业AI数据源配置
  - 支持RSS源和网页内容采集
  - 优先级和分类管理

### 固定输出
- **网页输出**: `result/index.html`
  - 响应式设计，适配多设备
  - 日期选择器，支持历史查看
  - 实时统计信息显示

- **Markdown输出**: `result/latest.md`
  - 简化版格式，适合分享
  - 包含标题、摘要、点评、链接
  - 标准化的分享格式

- **数据源统计**: `source/resultAI.xlsx`
  - 记录各数据源获取情况
  - 获取简讯数量统计
  - 失败原因分析
  - 最新简讯发布时间记录

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- 网络连接（用于数据采集）

### 2. 安装依赖
```bash
# 安装核心依赖
pip install pandas feedparser beautifulsoup4 requests openpyxl

# 或使用requirements.txt
pip install -r requirements.txt
```

### 3. 运行系统
```bash
# 测试运行（模拟数据）
python main_enhanced.py --test

# 完整运行（真实数据采集）
python main_enhanced.py

# 带参数运行
python main_enhanced.py --max-sources 10
```

### 4. 查看结果
- **网页版**: 打开 `result/index.html`
- **文本版**: 查看 `result/latest.md`
- **数据版**: 查看 `result/latest.json`
- **统计版**: 查看 `source/resultAI.xlsx`

## 📁 项目结构

```
Demo2/
├── main_enhanced.py              # 主程序入口
├── source/                       # 数据源管理
│   ├── AI_sources_updated.py     # 增强版数据源管理器
│   ├── AI_sources.xlsx          # 数据源配置（24个专业源）
│   └── resultAI.xlsx            # 数据源统计结果
├── crawler_enhanced.py          # 增强版数据采集器
├── result/                       # 输出结果
│   ├── index_optimized.html     # 优化后的网页模板
│   ├── index.html               # 主页面（固定输出）
│   ├── latest.md                # Markdown报告（固定输出）
│   ├── latest.json              # JSON数据文件
│   ├── 每日AI洞察简讯_*.md       # 详细Markdown报告
│   └── history/                 # 历史存档（30天）
├── data/                         # 原始数据
│   └── raw_articles_*.json       # 原始采集数据
├── .github/workflows/           # GitHub Actions配置
│   └── daily-fetch.yml          # 定时任务配置
└── requirements.txt             # 依赖包列表
```

## ⚙️ 配置说明

### 1. 数据源配置 (source/AI_sources.xlsx)

Excel文件包含以下列：
- `name`: 数据源名称（如：AWS blog、阿里云等）
- `type`: 数据源类型（rss/web）
- `rss_url`: RSS地址（优先使用）
- `home_url`: 网页URL（备用）
- `category`: 分类（11个固定分类）
- `priority`: 优先级（1-10）
- `enabled`: 是否启用（1/0）

### 2. 11个固定分类

1. **大模型**: LLM、GPT、千问、文心一言、通义等
2. **AI Agent**: 智能体、Agent平台、自动化等
3. **算力**: GPU、TPU、AI芯片、计算卡、数据中心等
4. **政策合规**: 政策、法规、标准、监管、安全等
5. **行业方案**: 行业应用、解决方案、落地案例等
6. **云计算**: 云服务、云平台、云原生、云安全等
7. **开源**: 开源项目、开源工具、开源框架等
8. **商业化**: 商业模式、商业应用、市场机会等
9. **安全**: 网络安全、数据安全、应用安全等
10. **企业服务**: 企业应用、企业软件、企业平台等
11. **技术趋势**: 技术发展、技术创新、技术突破等

## 📊 数据源统计说明

### resultAI.xlsx 文件结构

| 字段 | 说明 | 示例 |
|------|------|------|
| name | 数据源名称 | AWS blog |
| type | 数据源类型 | rss |
| category | 分类 | 云计算 |
| priority | 优先级 | 10 |
| article_count | 获取文章数 | 5 |
| status | 获取状态 | 成功/失败 |
| latest_publish_time | 最新发布时间 | 2026-03-07 09:30 |
| failure_reason | 失败原因 | 网页加载失败/无今日简讯 |

### 失败原因分类

1. **无今日简讯**: 数据源最新文章发布时间不满足今日要求
2. **网页加载失败**: 网络问题或网站不可访问
3. **RSS解析失败**: RSS格式错误或无法解析
4. **内容提取失败**: 网页结构变化导致无法提取内容
5. **其他错误**: 未知的系统错误

## 🔄 定时任务配置

### 1. Windows任务计划程序

创建批处理文件 `setup_scheduler.bat`：
```batch
@echo off
echo 设置AI简讯生成系统定时任务...

# 创建8:00任务
schtasks /create /tn "AI简讯生成-8:00" /tr "python C:\Users\h604658591\Demo2\main_enhanced.py" /sc daily /st 08:00

# 创建8:30任务
schtasks /create /tn "AI简讯生成-8:30" /tr "python C:\Users\h604658591\Demo2\main_enhanced.py" /sc daily /st 08:30

echo 定时任务设置完成！
pause
```

### 2. GitHub Actions (推荐)

配置文件 `.github/workflows/daily-fetch.yml`：
```yaml
name: Daily AI Insights
on:
  schedule:
    - cron: '0 0 * * *'  # 每天UTC时间0:00（北京时间8:00）
    - cron: '30 0 * * *' # 每天UTC时间0:30（北京时间8:30）
  workflow_dispatch:     # 支持手动触发

jobs:
  generate-insights:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run AI Insights Generator
        run: python main_enhanced.py
      - name: Commit and push if changed
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add result/ source/resultAI.xlsx
          git commit -m "Update AI insights and statistics" || exit 0
          git push
```

## 🛠️ 使用参数

### main_enhanced.py 参数选项
```bash
# 测试模式（使用模拟数据）
python main_enhanced.py --test

# 限制数据源数量
python main_enhanced.py --max-sources 5

# 详细日志输出
python main_enhanced.py --verbose
```

## 📈 系统运行流程

1. **数据采集** → 从24个专业数据源获取AI新闻
2. **智能处理** → 去重、分类、优先级计算
3. **内容生成** → AI摘要和云厂商视角分析
4. **多格式输出** → 生成HTML、Markdown、JSON、Excel文件
5. **历史存档** → 自动保存30天历史数据
6. **统计记录** → 生成数据源获取情况统计

## 🎯 输出文件示例

### result/index.html 网页界面
- 响应式设计，适配多设备
- 日期选择器，支持历史查看
- 实时统计信息显示
- 一键分享功能

### result/latest.md 分享格式
```markdown
# AI简讯【2026年3月7日】

1、【AWS宣布Amazon Bedrock新增多项AI推理功能】
摘要：AWS宣布Amazon Bedrock新增多项功能，包括增强的推理能力和更灵活的模型配置选项。
点评：从云厂商视角看，AWS持续强化AI基础设施，这将进一步巩固其在云计算AI服务领域的领先地位。
原文链接：https://aws.amazon.com/blogs/aws/new-amazon-bedrock-features/

2、【NVIDIA发布新一代AI芯片，性能提升显著】
摘要：NVIDIA最新发布的AI芯片在计算性能和能效方面都有显著提升。
点评：作为AI硬件领导者，NVIDIA的技术迭代将推动整个AI行业的发展速度。
原文链接：https://blogs.nvidia.com/new-ai-chip/

详见原文网址：https://harker1544525153-lang.github.io/ai-insights/
```

### source/resultAI.xlsx 统计示例
| 数据源 | 类型 | 分类 | 文章数 | 状态 | 失败原因 |
|--------|------|------|--------|------|----------|
| AWS blog | rss | 云计算 | 5 | 成功 | - |
| 阿里云 | rss | 云计算 | 3 | 成功 | - |
| 36氪 | web | 技术趋势 | 0 | 失败 | 网页加载失败 |
| NVIDIA blog | rss | 算力 | 2 | 成功 | - |

## 🔧 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 使用国内镜像源
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

2. **数据采集失败**
   - 检查网络连接
   - 验证数据源URL是否有效
   - 查看日志文件获取详细错误信息

3. **输出文件未生成**
   - 检查文件权限
   - 验证输出目录是否存在
   - 查看系统日志

### 日志文件
- 系统运行日志：自动生成在控制台和日志文件中
- 数据源统计：记录在 `source/resultAI.xlsx` 中
- 错误详情：查看Python异常堆栈信息

## 📞 技术支持

如有问题或建议，请参考：
- 查看 `source/resultAI.xlsx` 获取数据源状态
- 检查系统日志获取详细错误信息
- 验证数据源配置是否正确

---

**每日自动获取AI简讯Agent** - 让AI行业资讯获取更智能、更高效！