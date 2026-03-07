# AI简讯自动更新系统

## 📋 系统概述

AI简讯自动更新系统是一个基于Python的自动化工具，用于每天定时获取AI行业最新资讯，生成HTML和Markdown格式的简讯，并自动发布到GitHub Pages。

### 🌐 在线访问
- **GitHub Pages**: https://harker1544525153-lang.github.io/ai-insights/
- **GitHub仓库**: https://github.com/harker1544525153-lang/ai-insights

## 🚀 系统功能

### 核心功能
- ✅ **多源数据获取**: 从23个专业数据源获取AI行业资讯
- ✅ **智能内容生成**: 自动生成HTML网页和Markdown文档
- ✅ **定时自动更新**: 每天8:00和8:30自动执行
- ✅ **GitHub自动发布**: 自动提交并推送到GitHub Pages
- ✅ **错误处理机制**: 完善的日志记录和错误处理

### 技术特性
- **发布时间修复**: 使用原文实际发布时间，而非当前日期
- **响应式设计**: 完美适配手机和电脑浏览器
- **历史数据管理**: 支持查看历史简讯记录
- **实时更新**: GitHub Pages自动部署，内容实时更新

## 📁 文件结构

```
Demo2/
├── scheduler.bat                    # 定时任务执行脚本
├── generate_fixed_news.py          # 修复版简讯生成器
├── generate_optimized_news.py      # 优化版简讯生成器
├── generate_todays_news.py         # 基础版简讯生成器
├── index.html                      # 主页面（由result/index.html覆盖）
├── latest.md                       # Markdown格式简讯
├── logs/                           # 定时任务日志目录
│   └── scheduler_YYYYMMDD_HHMM.log # 执行日志文件
├── result/
│   └── index.html                  # 生成的HTML页面
├── source/
│   ├── AI_sources.xlsx             # 数据源配置
│   └── resultAI.csv                # 数据源统计信息
└── README.md                       # 系统说明文档
```

## ⚙️ 系统配置

### 定时任务配置

#### Windows任务计划程序设置
- **任务名称**: AI简讯自动更新-08:00 / AI简讯自动更新-08:30
- **触发器**: 每天 8:00 和 8:30
- **操作**: 
  - **程序或脚本**: `cmd.exe`
  - **参数**: `/c "C:\Users\h604658591\Demo2\scheduler.bat"`
  - **起始于**: `C:\Users\h604658591\Demo2`

#### 手动执行定时任务
```batch
# 在Demo2目录下执行
scheduler.bat

# 或使用PowerShell
.\scheduler.bat

# 测试环境
.\test_auto_update.bat
```

### 环境要求
- **Python 3.6+**: 用于运行简讯生成脚本
- **Git**: 用于版本控制和GitHub推送
- **Windows系统**: 支持定时任务调度

## 🔄 工作流程

### 每日自动执行流程

1. **环境检查** (8:00/8:30)
   - 检查Python和Git环境
   - 创建当日日志文件

2. **简讯生成**
   - 运行 `generate_fixed_news.py`
   - 生成6条AI行业最新简讯
   - 创建HTML和Markdown文件

3. **Git操作**
   - 添加所有更改文件
   - 提交更改到本地仓库
   - 推送到GitHub远程仓库

4. **日志记录**
   - 记录执行过程和结果
   - 清理7天前的旧日志

### 手动执行流程

```bash
# 1. 生成最新简讯
python generate_fixed_news.py

# 2. 提交到Git
git add .
git commit -m "手动更新AI简讯: YYYY-MM-DD HH:MM"

# 3. 推送到GitHub
git push origin main
```

## 📊 数据源配置

### 数据源类型
系统支持23个专业数据源，包括：
- **一级源**: DeepGEO、AIWW、Deeptracker等AI专业平台
- **二级源**: Gartner、IDC、Forrester等国际研究机构
- **三级源**: 东方财富网、华尔街见闻、199it等财经媒体
- **四级源**: SimilarWeb、新榜等舆情流量平台

### 数据源管理
- **配置文件**: `source/AI_sources.xlsx`
- **统计文件**: `source/resultAI.csv`
- **自动更新**: 每次执行后自动更新统计信息

## 🎨 输出格式

### HTML输出 (`index.html`)
- **导航栏**: AI简讯 【YYYY-MM-DD】 + 历史选择器 + 分享按钮
- **简讯布局**: 标题 + (类别 + 来源 + 发布时间 + 阅读原文)
- **响应式设计**: 适配各种屏幕尺寸
- **深色主题**: 科技感界面设计

### Markdown输出 (`latest.md`)
- **结构化格式**: 清晰的标题层级
- **完整信息**: 标题、类别、来源、发布时间、摘要、点评
- **原文链接**: 直接链接到原始文章

## 🔧 故障排除

### 常见问题

#### 1. 定时任务不执行
- 检查任务计划程序中的任务状态
- 确认Python和Git已正确安装并添加到PATH
- 查看日志文件 `logs/scheduler_*.log`

#### 2. GitHub推送失败
- 检查网络连接
- 确认GitHub仓库权限
- 验证Git配置信息

#### 3. 简讯生成失败
- 检查Python环境
- 确认数据源文件存在
- 查看错误日志

### 日志文件位置
- **定时任务日志**: `logs/scheduler_YYYYMMDD_HHMM.log`
- **自动更新日志**: `auto_update.log`

## 📈 系统监控

### 执行状态监控
- **成功执行**: 日志文件记录完整流程
- **失败处理**: 错误信息记录和提示
- **性能监控**: 执行时间统计

### 数据质量监控
- **简讯数量**: 每次生成6条简讯
- **发布时间**: 使用原文实际发布时间
- **内容完整性**: 标题、摘要、点评完整

## 🔄 版本更新

### 当前版本特性
- ✅ 修复发布时间bug，使用原文实际发布时间
- ✅ 阅读原文跟随发布时间在同一行显示
- ✅ 导航栏标题显示日期
- ✅ 分享按钮左侧添加历史日期选择器
- ✅ 根目录index.html由result/index.html覆盖

### 更新历史
- **2026-03-07**: 修复发布时间bug，优化界面布局
- **2026-03-07**: 实现定时任务自动执行
- **2026-03-07**: 完善错误处理和日志记录

## 📞 技术支持

### 系统维护
- **定时任务**: 每天8:00和8:30自动执行
- **日志管理**: 自动清理7天前日志
- **错误处理**: 完善的异常处理机制

### 问题反馈
如遇系统问题，请检查：
1. 日志文件中的错误信息
2. Python和Git环境配置
3. 网络连接状态
4. GitHub仓库权限

---

## 🎯 使用说明

### 首次设置
1. 确保Python和Git已正确安装
2. 配置GitHub仓库访问权限
3. 设置Windows定时任务
4. 测试手动执行功能

### 日常维护
- 系统自动运行，无需人工干预
- 定期检查日志文件确认执行状态
- 监控GitHub Pages网站访问状态

### 紧急处理
如遇紧急问题，可手动执行：
```bash
# 紧急更新
python generate_fixed_news.py
git add .
git commit -m "紧急更新"
git push origin main
```

---

**系统状态**: ✅ 正常运行  
**最后更新**: 2026-03-07  
**版本**: v1.0  
**维护者**: AI简讯系统