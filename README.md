# AI简讯自动化系统（新版本）

基于AI_sources.xlsx数据源的智能AI简讯生成和自动化发布系统。

## 系统特点

- ✅ **智能数据源管理**：从Excel文件管理多个数据源
- ✅ **双模式获取**：支持RSS订阅和网站爬取两种方式
- ✅ **内容自动提炼**：自动生成标题、摘要、点评
- ✅ **结果追踪**：详细记录每个数据源的获取结果
- ✅ **自动化部署**：定时任务自动生成并发布到GitHub

## 文件结构

```
Demo2/
├── AI_sources.xlsx              # 数据源配置（核心文件）
├── ai_news_system.py            # 主程序
├── ai_news_automation.ps1       # 自动化脚本
├── ai_news_task.xml            # Windows任务计划配置
├── index.html                   # 生成的HTML页面
├── resultAI.xlsx               # 处理结果统计
├── ai_news_automation.log      # 执行日志
├── execution_report.txt        # 执行报告
└── README.md                   # 本文档
```

## 数据源配置

### AI_sources.xlsx格式

| 字段 | 说明 | 示例 |
|------|------|------|
| name | 数据源名称 | DeepGEO |
| rss_url | RSS订阅地址（可选） | https://deepgeo.org.cn/rss |
| home_url | 网站首页地址 | https://deepgeo.org.cn |
| category | 分类 | 大模型 |

### 支持的数据源类型

1. **RSS优先**：有RSS地址的数据源
2. **网站爬取**：无RSS地址的数据源
3. **混合模式**：RSS失败时自动切换到网站爬取

## 简讯内容标准

### 1. 标题提炼
- 移除标题党词汇（震惊、重磅、突发等）
- 简化表达，突出核心内容
- 限制长度在50字以内

### 2. 摘要生成（200-300字）
- 客观描述，不进行分析
- 包含主体 + 时间 + 核心动作 + 相关数据
- 基于原文内容自动提炼关键信息

### 3. 点评生成（2-3句话）
- 从云厂商视角进行分析
- 分析事件对行业影响、竞争格局、潜在发展趋势
- 避免口号式表达，提供专业见解

## 快速开始

### 1. 手动运行

```bash
# 生成AI简讯
python ai_news_system.py

# 执行完整自动化流程
powershell -ExecutionPolicy Bypass -File "ai_news_automation.ps1"
```

### 2. 检查生成结果

生成的文件：
- `index.html`：AI简讯网页
- `resultAI.xlsx`：数据源处理结果统计
- 执行日志和报告

## Windows定时任务设置

### 方法一：使用任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器：每天8:00
4. 操作：启动程序
5. 程序：`powershell.exe`
6. 参数：`-ExecutionPolicy Bypass -File "C:\Users\h604658591\Demo2\ai_news_automation.ps1"`

### 方法二：导入XML配置

1. 打开"任务计划程序"
2. 导入任务
3. 选择：`ai_news_task.xml`
4. 确认导入

### 休眠模式支持

系统支持在电脑休眠情况下自动运行：
- 设置`WakeToRun: true`
- 支持网络唤醒
- 30分钟执行时间限制

## 数据源处理逻辑

### 成功条件
1. 能够获取到文章内容
2. 文章发布时间在今日或前一个工作日
3. 内容提取和提炼成功

### 失败原因记录
- RSS地址访问失败
- 网站爬取失败
- 文章时间不满足要求
- 内容提取失败

## 技术架构

### 核心模块

1. **数据源管理**：Excel文件读写，支持动态配置
2. **内容获取**：RSS解析 + 网站爬取双模式
3. **内容处理**：标题提炼、摘要生成、点评生成
4. **结果统计**：Excel格式的结果追踪
5. **网页生成**：响应式HTML页面生成
6. **自动化部署**：GitHub自动提交

### 依赖库

- `pandas`：Excel文件处理
- `feedparser`：RSS订阅解析
- `beautifulsoup4`：HTML内容解析
- `requests`：HTTP请求

## 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --user pandas feedparser beautifulsoup4 requests
   ```

2. **数据源文件不存在**
   - 检查`AI_sources.xlsx`文件是否存在
   - 确认文件格式正确

3. **网络连接问题**
   - 检查网络连接
   - 确认防火墙设置
   - 验证代理配置

4. **GitHub推送失败**
   - 检查Git配置
   - 验证GitHub访问权限
   - 确认网络连接

### 日志文件

系统生成详细的日志文件：
- `ai_news_automation.log`：执行日志
- `execution_report.txt`：执行报告

## 自定义配置

### 修改数据源

编辑`AI_sources.xlsx`文件，添加或修改数据源：

1. 新增数据源行
2. 填写名称、RSS地址、首页地址、分类
3. 保存文件

### 调整内容标准

修改`ai_news_system.py`中的相关函数：

- `refine_title()`：标题提炼规则
- `generate_summary()`：摘要生成逻辑
- `generate_comment()`：点评生成角度

## 版本历史

### v2.0 (当前版本)
- 基于Excel数据源管理
- 支持RSS和网站爬取双模式
- 智能内容提炼功能
- 详细的结果统计
- 完整的自动化流程

### v1.0 (历史版本)
- 固定数据源配置
- 基础内容获取
- 简单网页生成

## 技术支持

如有问题，请检查：
1. 日志文件中的错误信息
2. 数据源配置是否正确
3. 网络连接是否正常
4. 依赖库是否安装完整

---

**系统状态**：✅ 正常运行  
**最后更新**：2026-03-11  
**版本**：v2.0