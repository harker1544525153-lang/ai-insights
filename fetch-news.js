// AI行业资讯抓取脚本
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

class NewsFetcher {
    constructor() {
        this.newsData = [];
        this.dataFile = path.join(__dirname, 'data', 'news.json');
        this.ensureDataDirectory();
    }

    ensureDataDirectory() {
        const dataDir = path.join(__dirname, 'data');
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }
    }

    async fetchAllNews() {
        console.log('开始抓取AI行业资讯...');
        
        try {
            // 并发抓取多个数据源
            const fetchPromises = [
                this.fetchDeepGEO(),
                this.fetchAIWW(),
                this.fetchGartner(),
                this.fetchIDC(),
                this.fetchForrester()
            ];

            const results = await Promise.allSettled(fetchPromises);
            
            // 合并所有成功的结果
            results.forEach((result, index) => {
                if (result.status === 'fulfilled' && result.value) {
                    this.newsData = this.newsData.concat(result.value);
                } else {
                    console.error(`数据源 ${index} 抓取失败:`, result.reason);
                }
            });

            // 去重和排序
            this.processNewsData();
            
            // 保存到文件
            await this.saveNewsData();
            
            console.log(`抓取完成，共获取 ${this.newsData.length} 条资讯`);
            return this.newsData;
            
        } catch (error) {
            console.error('抓取过程中发生错误:', error);
            throw error;
        }
    }

    async fetchDeepGEO() {
        try {
            // 模拟DeepGEO数据抓取
            const news = [
                {
                    id: this.generateId(),
                    title: "OpenAI发布新一代GPT-5模型，推理能力大幅提升",
                    summary: "OpenAI正式发布GPT-5，在数学推理、代码生成和复杂问题解决方面相比GPT-4有显著提升，参数量达到2万亿。",
                    source: "DeepGEO",
                    time: new Date().toISOString(),
                    url: "https://deepgeo.org.cn/news/gpt5-release",
                    sourceType: "deepgeo"
                },
                {
                    id: this.generateId(),
                    title: "DeepMind突破蛋白质折叠预测精度达98.7%",
                    summary: "DeepMind宣布其AlphaFold3模型在蛋白质结构预测方面取得重大突破，预测精度达到98.7%。",
                    source: "DeepGEO",
                    time: new Date().toISOString(),
                    url: "https://deepgeo.org.cn/research/alphafold3",
                    sourceType: "deepgeo"
                }
            ];
            
            return news;
        } catch (error) {
            console.error('DeepGEO抓取失败:', error);
            return [];
        }
    }

    async fetchAIWW() {
        try {
            // 模拟AIWW数据抓取
            const news = [
                {
                    id: this.generateId(),
                    title: "AIWW指数显示AI工具搜索量月环比增长42%",
                    summary: "AIWW平台数据显示，AI工具类产品搜索指数本月环比增长42%，ChatGPT、Midjourney等工具持续热门。",
                    source: "AIWW",
                    time: new Date().toISOString(),
                    url: "https://aiww.com/trends/tools-feb-2026",
                    sourceType: "aiww"
                },
                {
                    id: this.generateId(),
                    title: "全球AI投资2026年Q1达850亿美元",
                    summary: "风险投资数据显示，2026年第一季度全球AI领域投资总额达到850亿美元，创历史新高。",
                    source: "AIWW",
                    time: new Date().toISOString(),
                    url: "https://aiww.com/investment/q1-2026",
                    sourceType: "aiww"
                }
            ];
            
            return news;
        } catch (error) {
            console.error('AIWW抓取失败:', error);
            return [];
        }
    }

    async fetchGartner() {
        try {
            // 模拟Gartner数据抓取
            const news = [
                {
                    id: this.generateId(),
                    title: "Gartner：生成式AI将在未来2年内进入生产成熟期",
                    summary: "Gartner最新技术成熟度曲线显示，生成式AI技术预计在2028年进入生产成熟期，企业应开始制定相关战略。",
                    source: "Gartner",
                    time: new Date().toISOString(),
                    url: "https://gartner.com/hype-cycle/genai-2026",
                    sourceType: "gartner"
                },
                {
                    id: this.generateId(),
                    title: "AI在医疗诊断领域准确率超过人类专家",
                    summary: "最新研究显示，AI在医学影像诊断方面的准确率已达到96.2%，超过人类专家的94.7%。",
                    source: "Gartner",
                    time: new Date().toISOString(),
                    url: "https://gartner.com/ai-healthcare-diagnosis",
                    sourceType: "gartner"
                }
            ];
            
            return news;
        } catch (error) {
            console.error('Gartner抓取失败:', error);
            return [];
        }
    }

    async fetchIDC() {
        try {
            // 模拟IDC数据抓取
            const news = [
                {
                    id: this.generateId(),
                    title: "AI芯片市场2026年Q1增长35%，英伟达继续领跑",
                    summary: "根据IDC最新报告，全球AI芯片市场第一季度同比增长35%，英伟达市场份额达到85%，创历史新高。",
                    source: "IDC",
                    time: new Date().toISOString(),
                    url: "https://idc.com/reports/ai-chip-q1-2026",
                    sourceType: "idc"
                },
                {
                    id: this.generateId(),
                    title: "中国AI产业规模预计2026年突破2万亿元",
                    summary: "根据工信部数据，中国AI产业规模持续增长，预计2026年将突破2万亿元，年复合增长率达25%。",
                    source: "IDC",
                    time: new Date().toISOString(),
                    url: "https://idc.com/china-ai-market-2026",
                    sourceType: "idc"
                }
            ];
            
            return news;
        } catch (error) {
            console.error('IDC抓取失败:', error);
            return [];
        }
    }

    async fetchForrester() {
        try {
            // 模拟Forrester数据抓取
            const news = [
                {
                    id: this.generateId(),
                    title: "Forrester：67%的企业计划在年内部署AI助手",
                    summary: "Forrester消费者趋势报告显示，超过三分之二的企业计划在2026年内部署AI助手，提升客户服务效率。",
                    source: "Forrester",
                    time: new Date().toISOString(),
                    url: "https://forrester.com/ai-assistant-adoption",
                    sourceType: "forrester"
                },
                {
                    id: this.generateId(),
                    title: "AI伦理框架国际标准即将发布",
                    summary: "国际标准化组织宣布，AI伦理框架国际标准将于下月正式发布，为全球AI发展提供指导。",
                    source: "Forrester",
                    time: new Date().toISOString(),
                    url: "https://forrester.com/ai-ethics-standards",
                    sourceType: "forrester"
                }
            ];
            
            return news;
        } catch (error) {
            console.error('Forrester抓取失败:', error);
            return [];
        }
    }

    processNewsData() {
        // 去重（基于标题）
        const seenTitles = new Set();
        this.newsData = this.newsData.filter(news => {
            const normalizedTitle = news.title.toLowerCase().trim();
            if (seenTitles.has(normalizedTitle)) {
                return false;
            }
            seenTitles.add(normalizedTitle);
            return true;
        });

        // 按时间排序（最新的在前）
        this.newsData.sort((a, b) => new Date(b.time) - new Date(a.time));

        // 格式化时间
        this.newsData.forEach(news => {
            const date = new Date(news.time);
            news.time = date.toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }).replace(/\//g, '-');
        });
    }

    async saveNewsData() {
        const data = {
            lastUpdated: new Date().toISOString(),
            news: this.newsData
        };

        try {
            fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2), 'utf8');
            console.log('资讯数据已保存到文件');
        } catch (error) {
            console.error('保存数据失败:', error);
            throw error;
        }
    }

    generateId() {
        return Date.now() + Math.random().toString(36).substr(2, 9);
    }

    async loadExistingData() {
        try {
            if (fs.existsSync(this.dataFile)) {
                const data = JSON.parse(fs.readFileSync(this.dataFile, 'utf8'));
                return data.news || [];
            }
        } catch (error) {
            console.error('加载现有数据失败:', error);
        }
        return [];
    }

    // 增量更新模式（保留历史数据）
    async incrementalUpdate() {
        const existingNews = await this.loadExistingData();
        const newNews = await this.fetchAllNews();
        
        // 合并新旧数据，新数据优先
        const allNews = [...newNews, ...existingNews];
        
        // 去重和排序
        const seenTitles = new Set();
        this.newsData = allNews.filter(news => {
            const normalizedTitle = news.title.toLowerCase().trim();
            if (seenTitles.has(normalizedTitle)) {
                return false;
            }
            seenTitles.add(normalizedTitle);
            return true;
        }).sort((a, b) => new Date(b.time) - new Date(a.time));

        await this.saveNewsData();
        return this.newsData;
    }
}

// 命令行接口
if (require.main === module) {
    const fetcher = new NewsFetcher();
    
    const args = process.argv.slice(2);
    const mode = args[0] || 'full'; // full 或 incremental
    
    async function run() {
        try {
            if (mode === 'incremental') {
                console.log('执行增量更新模式...');
                await fetcher.incrementalUpdate();
            } else {
                console.log('执行全量更新模式...');
                await fetcher.fetchAllNews();
            }
            
            console.log('任务完成！');
            process.exit(0);
        } catch (error) {
            console.error('任务失败:', error);
            process.exit(1);
        }
    }
    
    run();
}

module.exports = NewsFetcher;