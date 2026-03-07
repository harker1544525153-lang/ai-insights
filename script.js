// AI行业每日简讯 - 前端交互脚本

class AINewsApp {
    constructor() {
        this.newsData = [];
        this.selectedSources = new Set(['deepgeo', 'aiww', 'gartner', 'idc', 'forrester']);
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.displayCurrentDate();
        this.loadNews();
        this.loadSettings();
    }

    setupEventListeners() {
        // 刷新按钮
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshNews();
        });

        // 分享按钮
        document.getElementById('shareBtn').addEventListener('click', () => {
            this.showShareModal();
        });

        // 管理资讯源按钮
        document.getElementById('manageSourcesBtn').addEventListener('click', () => {
            this.showSourceModal();
        });

        // 模态框关闭按钮
        document.getElementById('closeModal').addEventListener('click', () => {
            this.hideSourceModal();
        });

        document.getElementById('closeShareModal').addEventListener('click', () => {
            this.hideShareModal();
        });

        // 保存资讯源设置
        document.getElementById('saveSources').addEventListener('click', () => {
            this.saveSourceSettings();
        });

        // 添加自定义资讯源
        document.getElementById('addCustomSource').addEventListener('click', () => {
            this.addCustomSource();
        });

        // 分享选项
        document.querySelectorAll('.share-option').forEach(option => {
            option.addEventListener('click', (e) => {
                this.handleShare(e.target.closest('.share-option').dataset.type);
            });
        });

        // 点击模态框外部关闭
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });

        // 键盘事件
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideAllModals();
            }
        });
    }

    displayCurrentDate() {
        const now = new Date();
        const dateStr = now.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long'
        });
        
        const timeStr = now.toLocaleTimeString('zh-CN', {
            hour: '2-digit',
            minute: '2-digit'
        });

        document.getElementById('currentDate').textContent = dateStr;
        document.getElementById('updateTime').textContent = `更新时间: ${timeStr}`;
        document.getElementById('lastUpdate').textContent = `${dateStr} ${timeStr}`;
    }

    async loadNews() {
        try {
            // 模拟从本地JSON文件加载数据
            const response = await fetch('data/news.json');
            if (response.ok) {
                this.newsData = await response.json();
                this.renderNews();
            } else {
                // 如果本地数据不存在，使用模拟数据
                this.useMockData();
            }
        } catch (error) {
            console.error('加载新闻数据失败:', error);
            this.useMockData();
        }
    }

    useMockData() {
        // 模拟AI行业新闻数据
        this.newsData = [
            {
                id: 1,
                title: "OpenAI发布新一代GPT-5模型，推理能力大幅提升",
                summary: "OpenAI正式发布GPT-5，在数学推理、代码生成和复杂问题解决方面相比GPT-4有显著提升，参数量达到2万亿。",
                source: "DeepGEO",
                time: "2026-02-26 09:30",
                url: "https://deepgeo.org.cn/news/gpt5-release",
                sourceType: "deepgeo"
            },
            {
                id: 2,
                title: "AI芯片市场2026年Q1增长35%，英伟达继续领跑",
                summary: "根据IDC最新报告，全球AI芯片市场第一季度同比增长35%，英伟达市场份额达到85%，创历史新高。",
                source: "IDC",
                time: "2026-02-26 10:15",
                url: "https://idc.com/reports/ai-chip-q1-2026",
                sourceType: "idc"
            },
            {
                id: 3,
                title: "Gartner：生成式AI将在未来2年内进入生产成熟期",
                summary: "Gartner最新技术成熟度曲线显示，生成式AI技术预计在2028年进入生产成熟期，企业应开始制定相关战略。",
                source: "Gartner",
                time: "2026-02-26 11:00",
                url: "https://gartner.com/hype-cycle/genai-2026",
                sourceType: "gartner"
            },
            {
                id: 4,
                title: "AIWW指数显示AI工具搜索量月环比增长42%",
                summary: "AIWW平台数据显示，AI工具类产品搜索指数本月环比增长42%，ChatGPT、Midjourney等工具持续热门。",
                source: "AIWW",
                time: "2026-02-26 14:20",
                url: "https://aiww.com/trends/tools-feb-2026",
                sourceType: "aiww"
            },
            {
                id: 5,
                title: "Forrester：67%的企业计划在年内部署AI助手",
                summary: "Forrester消费者趋势报告显示，超过三分之二的企业计划在2026年内部署AI助手，提升客户服务效率。",
                source: "Forrester",
                time: "2026-02-26 15:45",
                url: "https://forrester.com/ai-assistant-adoption",
                sourceType: "forrester"
            },
            {
                id: 6,
                title: "DeepMind突破蛋白质折叠预测精度达98.7%",
                summary: "DeepMind宣布其AlphaFold3模型在蛋白质结构预测方面取得重大突破，预测精度达到98.7%。",
                source: "DeepGEO",
                time: "2026-02-26 16:30",
                url: "https://deepgeo.org.cn/research/alphafold3",
                sourceType: "deepgeo"
            },
            {
                id: 7,
                title: "中国AI产业规模预计2026年突破2万亿元",
                summary: "根据工信部数据，中国AI产业规模持续增长，预计2026年将突破2万亿元，年复合增长率达25%。",
                source: "IDC",
                time: "2026-02-26 17:15",
                url: "https://idc.com/china-ai-market-2026",
                sourceType: "idc"
            },
            {
                id: 8,
                title: "AI在医疗诊断领域准确率超过人类专家",
                summary: "最新研究显示，AI在医学影像诊断方面的准确率已达到96.2%，超过人类专家的94.7%。",
                source: "Gartner",
                time: "2026-02-26 18:00",
                url: "https://gartner.com/ai-healthcare-diagnosis",
                sourceType: "gartner"
            },
            {
                id: 9,
                title: "全球AI投资2026年Q1达850亿美元",
                summary: "风险投资数据显示，2026年第一季度全球AI领域投资总额达到850亿美元，创历史新高。",
                source: "AIWW",
                time: "2026-02-26 19:30",
                url: "https://aiww.com/investment/q1-2026",
                sourceType: "aiww"
            },
            {
                id: 10,
                title: "AI伦理框架国际标准即将发布",
                summary: "国际标准化组织宣布，AI伦理框架国际标准将于下月正式发布，为全球AI发展提供指导。",
                source: "Forrester",
                time: "2026-02-26 20:15",
                url: "https://forrester.com/ai-ethics-standards",
                sourceType: "forrester"
            }
        ];
        
        this.renderNews();
    }

    renderNews() {
        const newsGrid = document.getElementById('newsGrid');
        
        // 过滤选中的资讯源
        const filteredNews = this.newsData.filter(news => 
            this.selectedSources.has(news.sourceType)
        );

        if (filteredNews.length === 0) {
            newsGrid.innerHTML = `
                <div class="loading">
                    <p>暂无符合筛选条件的资讯</p>
                    <p>请检查资讯源设置</p>
                </div>
            `;
            return;
        }

        // 渲染新闻卡片
        newsGrid.innerHTML = filteredNews.map(news => `
            <div class="news-card" data-id="${news.id}">
                <div class="news-header">
                    <span class="source-tag">${news.source}</span>
                </div>
                <h3 class="news-title">${news.title}</h3>
                <p class="news-summary">${news.summary}</p>
                <div class="news-meta">
                    <span class="news-time">${news.time}</span>
                    <a href="${news.url}" target="_blank" class="news-link" rel="noopener noreferrer">
                        查看详情 →
                    </a>
                </div>
            </div>
        `).join('');

        // 添加点击事件
        document.querySelectorAll('.news-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.news-link')) {
                    const newsId = card.dataset.id;
                    const news = this.newsData.find(n => n.id == newsId);
                    if (news) {
                        window.open(news.url, '_blank', 'noopener,noreferrer');
                    }
                }
            });
        });
    }

    refreshNews() {
        const refreshBtn = document.getElementById('refreshBtn');
        const originalText = refreshBtn.innerHTML;
        
        // 显示加载状态
        refreshBtn.innerHTML = '<span class="btn-icon">⏳</span>刷新中...';
        refreshBtn.disabled = true;

        // 模拟刷新过程
        setTimeout(() => {
            this.displayCurrentDate();
            this.loadNews();
            
            // 恢复按钮状态
            refreshBtn.innerHTML = originalText;
            refreshBtn.disabled = false;
            
            // 显示成功提示
            this.showToast('资讯已刷新', 'success');
        }, 1500);
    }

    showSourceModal() {
        const modal = document.getElementById('sourceModal');
        
        // 更新复选框状态
        document.querySelectorAll('.source-item input').forEach(checkbox => {
            checkbox.checked = this.selectedSources.has(checkbox.dataset.source);
        });
        
        modal.style.display = 'block';
    }

    hideSourceModal() {
        document.getElementById('sourceModal').style.display = 'none';
    }

    saveSourceSettings() {
        const selectedSources = new Set();
        
        document.querySelectorAll('.source-item input:checked').forEach(checkbox => {
            selectedSources.add(checkbox.dataset.source);
        });
        
        this.selectedSources = selectedSources;
        this.saveSettings();
        this.renderNews();
        this.hideSourceModal();
        
        this.showToast('资讯源设置已保存', 'success');
    }

    addCustomSource() {
        const urlInput = document.getElementById('customSourceUrl');
        const url = urlInput.value.trim();
        
        if (!url) {
            this.showToast('请输入有效的URL地址', 'error');
            return;
        }
        
        // 简单的URL验证
        try {
            new URL(url);
            this.showToast('自定义资讯源已添加', 'success');
            urlInput.value = '';
            
            // 在实际应用中，这里会保存到设置中
        } catch (error) {
            this.showToast('请输入有效的URL地址', 'error');
        }
    }

    showShareModal() {
        const modal = document.getElementById('shareModal');
        
        // 生成分享文本
        const shareText = this.generateShareText();
        document.getElementById('shareText').value = shareText;
        
        modal.style.display = 'block';
    }

    hideShareModal() {
        document.getElementById('shareModal').style.display = 'none';
    }

    hideAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
    }

    generateShareText() {
        const filteredNews = this.newsData.filter(news => 
            this.selectedSources.has(news.sourceType)
        ).slice(0, 10); // 取前10条
        
        let shareText = `AI行业每日简讯 - 今日十大精选\n\n`;
        
        filteredNews.forEach((news, index) => {
            shareText += `${index + 1}. ${news.title}\n`;
            shareText += `   ${news.summary}\n\n`;
        });
        
        shareText += `查看完整内容：${window.location.href}\n`;
        shareText += `分享时间：${new Date().toLocaleString('zh-CN')}`;
        
        return shareText;
    }

    handleShare(type) {
        const shareText = document.getElementById('shareText').value;
        
        switch (type) {
            case 'wechat':
                this.shareToWechat(shareText);
                break;
            case 'weibo':
                this.shareToWeibo(shareText);
                break;
            case 'copy':
                this.copyToClipboard(shareText);
                break;
        }
    }

    shareToWechat(text) {
        // 模拟微信分享
        this.showToast('请使用微信扫一扫分享', 'info');
    }

    shareToWeibo(text) {
        // 微博分享
        const url = `https://service.weibo.com/share/share.php?title=${encodeURIComponent(text)}&url=${encodeURIComponent(window.location.href)}`;
        window.open(url, '_blank', 'width=600,height=400');
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('已复制到剪贴板', 'success');
        } catch (err) {
            // 降级方案
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('已复制到剪贴板', 'success');
        }
    }

    showToast(message, type = 'info') {
        // 移除现有的toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }

        // 创建新的toast
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // 添加样式
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ff6b6b' : type === 'success' ? '#51cf66' : '#339af0'};
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // 3秒后自动移除
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    saveSettings() {
        const settings = {
            selectedSources: Array.from(this.selectedSources),
            lastUpdate: new Date().toISOString()
        };
        localStorage.setItem('aiNewsSettings', JSON.stringify(settings));
    }

    loadSettings() {
        const saved = localStorage.getItem('aiNewsSettings');
        if (saved) {
            try {
                const settings = JSON.parse(saved);
                if (settings.selectedSources) {
                    this.selectedSources = new Set(settings.selectedSources);
                }
            } catch (error) {
                console.error('加载设置失败:', error);
            }
        }
    }
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .news-card {
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
`;
document.head.appendChild(style);

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new AINewsApp();
});