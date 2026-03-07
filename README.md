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
```

### 3. 运行系统
```bash
# 手动运行简讯生成
python get_latest_insights.py

# 测试数据源统计管理器
python source/simple_result_ai_manager.py

# 或使用完整系统
python run.py
```

## ⚙️ 全流程定时生成与GitHub上传流程

### 📅 定时生成流程

#### 1. 数据采集阶段
```python
# 从配置的数据源采集数据
- 读取 source/AI_sources.xlsx 配置
- 按优先级顺序访问各数据源
- 支持RSS源和网页内容采集
- 自动处理网络异常和超时
```

#### 2. 内容处理阶段
```python
# 智能内容处理流程
- 日期筛选：仅保留今日及昨日内容
- 去重处理：基于标题和链接去重
- 智能分类：11大固定分类匹配
- 优先级计算：技术变化、商机、成本等维度
- 内容生成：200-300字摘要 + 云厂商视角点评
```

#### 3. 输出生成阶段
```python
# 多格式文件生成
- Markdown格式：result/latest.md
- HTML网页：result/index.html
- 数据统计：source/resultAI.csv
- 历史存档：result/history/YYYY-MM-DD.html
```

#### 4. GitHub自动上传
```bash
# 自动提交到GitHub
- 检查文件变更：git status
- 添加变更文件：git add result/ source/
- 提交变更：git commit -m "更新AI简讯 YYYY-MM-DD"
- 推送到远程：git push origin main
```

### 🔄 自动化定时任务配置

#### GitHub Actions配置 (推荐)
```yaml
# .github/workflows/daily-fetch.yml
name: 每日AI简讯生成
on:
  schedule:
    - cron: '0 0 * * *'  # 每天UTC时间00:00（北京时间08:00）
    - cron: '30 0 * * *' # 每天UTC时间00:30（北京时间08:30）
  workflow_dispatch:  # 支持手动触发

jobs:
  generate-insights:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 设置Python环境
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: 安装依赖
        run: pip install pandas feedparser requests openpyxl
      - name: 生成AI简讯
        run: python get_latest_insights.py
      - name: 提交到GitHub
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add result/ source/
          git commit -m "自动更新AI简讯 $(date +'%Y-%m-%d')" || exit 0
          git push
```

#### Windows任务计划程序
```batch
# setup_scheduler.bat
@echo off
echo 设置每日AI简讯自动生成任务
schtasks /create /tn "每日AI简讯生成" /tr "python C:\path\to\get_latest_insights.py" /sc daily /st 08:00 /ru "SYSTEM"
echo 任务设置完成
```

## 📊 数据源统计规范

### resultAI数据表格式

当仅获取到部分数据源信息时，resultAI表格将**仅呈现成功获取的数据源信息**，确保数据准确性。

系统使用 `source/simple_result_ai_manager.py` 来管理数据源统计，该模块具有以下特点：

- **不依赖外部库**：使用Python标准库实现，无需安装pandas等依赖
- **智能数据呈现**：仅显示实际处理过的数据源，避免空数据干扰
- **多格式输出**：同时生成CSV和JSON格式，便于不同场景使用
- **优先级排序**：按数据源优先级自动排序，高优先级在前

#### 表格结构
| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| name | 文本 | 数据源名称 | 阿里云（微信公众号） |
| type | 文本 | 数据源类型 | rss |
| rss_url | 文本 | RSS地址 | https://wechatrss.waytomaster.com/api/rss/... |
| home_url | 文本 | 主页地址 | https://mp.weixin.qq.com/ |
| category | 文本 | 主要分类 | 云计算 |
| priority | 数字 | 优先级(1-10) | 10 |
| enabled | 布尔 | 是否启用 | 1 |
| 获取简讯数 | 数字 | 成功获取的简讯数量 | 3 |
| 获取结果 | 文本 | 获取状态说明 | 成功获取今日简讯 |
| 生成时间 | 时间 | 数据生成时间 | 2026-03-07 18:16:35 |

#### 部分数据源获取示例
当系统仅成功获取部分数据源时，resultAI表格将显示：

```csv
name,type,rss_url,home_url,category,priority,enabled,获取简讯数,获取结果,生成时间
阿里云（微信公众号）,rss,https://wechatrss.waytomaster.com/api/rss/...,,云计算,10,1,3,成功获取今日简讯,2026-03-07 18:16:35
腾讯研究院（微信公众号）,rss,https://wechatrss.waytomaster.com/api/rss/...,,技术趋势,10,1,0,最新文章时间2026-03-06，不满足今日要求,2026-03-07 18:16:35
AWS blog,rss,https://aws.amazon.com/blogs/aws/feed/,https://aws.amazon.com/blogs/,云计算,10,1,0,rss_url地址访问失败，导致无数据,2026-03-07 18:16:35
```

### 获取结果状态说明

#### 成功状态
- `成功获取今日简讯`：正常获取到今日内容
- `获取到历史简讯`：获取到非今日但有价值的内容

#### 失败状态
- `最新文章时间YYYY-MM-DD，不满足今日要求`：内容发布时间不符合要求
- `rss_url地址访问失败，导致无数据`：网络或地址问题
- `数据源暂时不可用`：服务器维护或限制
- `内容格式解析失败`：HTML/RSS格式异常

## 🎨 固定生成样式与内容格式

### HTML网页样式规范

#### 导航栏设计
```html
<div class="navbar">
    <div class="navbar-title">AI简讯</div>
    <div class="navbar-controls">
        <select class="date-selector" id="dateSelector">
            <option value="当前日期">当前日期</option>
        </select>
        <button class="share-btn" onclick="shareContent()">分享</button>
        <button class="history-btn" onclick="openHistoryModal()">历史数据</button>
    </div>
</div>
```

#### 简讯预览区域
- **高度限制**: 200-300px，显示所有标题不滑动
- **标题格式**: 纯文本序号 + 标题 + 分类标签
- **间距设计**: 标题之间紧凑排列

#### 详细简讯格式
```html
<div class="insight">
    <div class="insight-header">
        <div class="insight-title">序号. 标题</div>
        <div class="insight-link">
            <a href="原文链接" target="_blank" class="read-link">阅读原文</a>
        </div>
    </div>
    <div class="insight-meta">
        分类：类别 | 来源：数据源 | 发布时间：YYYY-MM-DD HH:MM
    </div>
    <div class="insight-summary">200-300字客观摘要</div>
    <div class="insight-comment">2-3句云厂商视角点评</div>
</div>
```

### Markdown内容格式规范

#### 标题格式
```markdown
# AI简讯【YYYY-MM-DD】

## 今日简讯概览（基于真实数据源）

1. **标题** - 分类 - 发布时间
2. **标题** - 分类 - 发布时间
```

#### 详细内容格式
```markdown
### 1、标题
**分类：** 云计算  
**来源：** 阿里云（微信公众号）  
**发布时间：** YYYY-MM-DD HH:MM  

**摘要：** 200-300字客观描述，包含主体+时间+核心动作+相关数据

**点评：** 2-3句云厂商视角分析，关注行业影响、竞争格局、发展趋势

**原文链接：** https://example.com
```

## 🔧 数据源配置优化

### AI_sources.xlsx配置规范

#### 数据源筛选规则
1. **优先级排序**: 按priority字段降序排列
2. **启用状态**: 仅处理enabled=1的数据源
3. **类型支持**: 优先处理RSS源，其次网页爬取
4. **分类匹配**: 根据category字段进行内容分类

#### 失败处理机制
- **网络异常**: 自动重试3次，间隔5秒
- **格式错误**: 跳过无法解析的数据源
- **时间过滤**: 仅保留今日及昨日内容
- **去重处理**: 基于标题和链接去重

## 📈 监控与日志

### 运行统计信息
每次运行后输出以下统计：
- 开始时间和结束时间
- 运行时长
- 处理源数量
- 获取文章数
- 筛选后文章数
- 最终文章数
- 分类统计
- 错误信息（如有）

### 日志文件
- **运行日志**: 记录每次执行的详细过程
- **错误日志**: 记录失败原因和异常信息
- **数据日志**: 记录各数据源的获取状态

## 🚨 故障排除

### 常见问题

#### 1. 数据源获取失败
- **检查网络连接**
- **验证RSS地址有效性**
- **检查数据源是否维护**

#### 2. GitHub上传失败
- **检查Git配置**
- **验证SSH密钥或Token**
- **检查文件权限**

#### 3. 定时任务不执行
- **检查系统时间设置**
- **验证任务计划程序状态**
- **检查Python环境路径**

### 联系方式
如有问题，请通过GitHub Issues提交反馈。

---

**最后更新**: 2026-03-07  
**版本**: v3.0  
**维护者**: AI简讯自动化系统