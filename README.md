# AI行业每日简讯

🤖 一个智能的AI行业资讯聚合平台，每日自动更新最新的AI技术动态、市场趋势和行业洞察。

## ✨ 功能特性

- **多源聚合**: 整合DeepGEO、AIWW、Gartner、IDC等权威平台的AI行业资讯
- **自动更新**: 通过GitHub Actions每日定时抓取最新资讯
- **响应式设计**: 完美适配手机、平板和电脑端
- **自定义筛选**: 支持按资讯源筛选，可添加自定义RSS源
- **一键分享**: 支持分享今日十大精选资讯到微信、微博等平台
- **实时更新**: 前端自动刷新，确保信息时效性

## 🚀 快速开始

### 本地运行

1. **克隆项目**
```bash
git clone https://github.com/your-username/ai-daily-news.git
cd ai-daily-news
```

2. **安装依赖**
```bash
npm install
```

3. **启动本地服务器**
```bash
# 使用Python简单服务器
python -m http.server 8000

# 或使用Node.js的http-server
npx http-server -p 8000
```

4. **访问应用**
打开浏览器访问 `http://localhost:8000`

### 数据抓取测试

```bash
# 全量抓取（测试用）
node fetch-news.js full

# 增量抓取（生产用）
node fetch-news.js incremental
```

## 📁 项目结构

```
ai-daily-news/
├── index.html              # 主页面
├── style.css               # 样式文件
├── script.js               # 前端交互逻辑
├── fetch-news.js           # 后端数据抓取脚本
├── package.json            # 项目配置
├── data/
│   └── news.json           # 资讯数据文件（自动生成）
├── .github/
│   └── workflows/
│       └── daily-fetch.yml # GitHub Actions定时任务
└── README.md               # 项目说明
```

## 🔧 配置说明

### 资讯源配置

项目支持以下默认资讯源：

- **DeepGEO** - AI产品搜索指数和热度排行
- **AIWW** - AI行业指数和软件工具排行  
- **Gartner** - 技术成熟度曲线和新兴趋势
- **IDC** - 全球IT市场份额和预测报告
- **Forrester** - 消费者趋势分析

### 自定义资讯源

在管理界面可以添加自定义RSS源或API接口：

1. 点击底部"管理资讯源"按钮
2. 在输入框中填入RSS地址或API端点
3. 保存设置即可生效

### GitHub Actions配置

定时任务每天UTC时间0点（北京时间8点）自动执行：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天UTC午夜
```

## 🌐 部署指南

### GitHub Pages部署

1. 在GitHub仓库设置中开启GitHub Pages
2. 选择部署源为"GitHub Actions"
3. 推送代码到main分支即可自动部署

### 其他部署方式

项目为纯静态页面，可部署到任何静态网站托管服务：

- **Vercel**: `vercel --prod`
- **Netlify**: 直接拖拽dist文件夹
- **阿里云OSS**: 上传文件到对象存储
- **腾讯云COS**: 配置静态网站托管

## 🔍 数据源说明

### 一级数据源（核心）
- **DeepGEO**: AI产品搜索指数、热度排行
- **AIWW**: AI行业指数、软件工具排行
- **Deeptracker**: 企业动态、供应链预警

### 二级数据源（国际研究）
- **Gartner**: 技术成熟度曲线、新兴趋势
- **IDC**: 全球IT市场份额、预测报告  
- **Forrester**: 消费者趋势分析
- **尼尔森IQ**: 消费行为洞察

### 三级数据源（财经媒体）
- **东方财富网**: 行业研报、公司财报
- **华尔街见闻**: 全球化视野解读
- **199it**: 聚合行业报告
- **亿欧智库**: 科技产业研究

## 📊 技术架构

### 前端技术栈
- **HTML5**: 语义化标记
- **CSS3**: 响应式布局、渐变效果、动画
- **JavaScript ES6+**: 模块化编程、异步处理
- **LocalStorage**: 本地设置存储

### 后端技术栈
- **Node.js**: 运行时环境
- **Axios**: HTTP请求库
- **Cheerio**: 服务器端DOM解析
- **GitHub Actions**: 自动化部署和定时任务

## 🔒 安全考虑

- 所有外部链接使用 `rel="noopener noreferrer"`
- 资讯源配置支持HTTPS验证
- 用户设置存储在本地，不涉及服务器
- 定时任务使用GitHub Secrets管理敏感信息

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发流程

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范

- 使用ES6+语法
- 遵循语义化版本控制
- 提交信息使用约定式提交格式
- 确保响应式设计兼容性

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢以下平台提供的API和数据支持：

- [DeepGEO](https://deepgeo.org.cn) - AI产品搜索指数
- [AIWW](https://aiww.com) - AI行业指数
- [Gartner](https://gartner.com) - 技术成熟度曲线
- [IDC](https://idc.com) - 市场研究报告

## 📞 联系方式

- 项目主页: [GitHub Repository](https://github.com/your-username/ai-daily-news)
- 问题反馈: [Issues](https://github.com/your-username/ai-daily-news/issues)
- 邮箱: your-email@example.com

---

⭐ 如果这个项目对你有帮助，请给它一个Star！