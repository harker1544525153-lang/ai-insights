import requests
import json
import os
from datetime import datetime

# 获取最新资讯的函数
def fetch_news():
    # 这里实现获取资讯的逻辑
    # 例如从各个数据源获取最新资讯
    # 以下是示例数据
    news_data = [
        {
            "id": 1,
            "title": "示例资讯1",
            "content": "这是示例资讯内容1",
            "source": "示例来源",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "link": "https://example.com/news1"
        },
        # 更多资讯...
    ]
    return news_data

# 生成HTML文件
def generate_html(news):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日AI行业洞察·十大精选</title>
    <style>
        /* 样式代码与之前相同 */
        :root {{
            --primary-color: #6366f1;
            --secondary-color: #8b5cf6;
            --background-color: #0f172a;
            --card-background: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --border-color: #334155;
            --success-color: #10b981;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background-color);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        }}

        .refresh-btn-container {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }}

        .refresh-btn, .share-btn {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .refresh-btn:hover, .share-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        }}

        .refresh-icon, .share-icon {{
            width: 20px;
            height: 20px;
        }}

        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }}

        .news-card {{
            background-color: var(--card-background);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .news-card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-color);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }}

        .news-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        }}

        .news-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .news-content {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}

        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}

        .news-source {{
            background-color: rgba(99, 102, 241, 0.1);
            color: var(--primary-color);
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 500;
        }}

        .news-link {{
            display: inline-block;
            color: var(--primary-color);
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: color 0.3s ease;
        }}

        .news-link:hover {{
            color: var(--secondary-color);
            text-decoration: underline;
        }}

        footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .loading {{
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }}

        .toast {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: var(--success-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }}

        .toast.show {{
            transform: translateX(0);
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            h1 {{
                font-size: 2rem;
            }}

            .news-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>每日AI行业洞察·十大精选 · {current_date}</h1>
            <div class="refresh-btn-container">
                <button id="refreshBtn" class="refresh-btn">
                    <svg class="refresh-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z"></path>
                    </svg>
                    获取最新资讯
                </button>
                <button id="shareBtn" class="share-btn">
                    <svg class="share-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18,16.08C17.24,16.08 16.56,16.38 16.04,16.85L8.91,12.7C8.96,12.47 9,12.24 9,12C9,11.76 8.96,11.53 8.91,11.3L15.96,7.19C16.5,7.69 17.21,8 18,8A3,3 0 0,0 21,5A3,3 0 0,0 18,2C15.65,2 13.73,3.66 13.35,5.93L7.39,9.34C6.54,9.76 6,10.56 6,11.5V16A2,2 0 0,0 8,18H13.5A2.5,2.5 0 0,0 16,15.5V11.22L18,12.3V16.08M15,13.5A1,1 0 0,1 14,14.5V17H9V15H13V14.5A1,1 0 0,1 15,13.5Z"></path>
                    </svg>
                    分享资讯
                </button>
            </div>
        </header>

        <div id="newsContainer" class="news-grid">
            <!-- 新闻卡片将通过JavaScript动态生成 -->
        </div>

        <footer>
            <p>最近更新：{current_time}</p>
        </footer>
    </div>

    <div id="toast" class="toast">复制成功！</div>

    <script>
        // 新闻数据
        const newsData = {json.dumps(news)};

        // 渲染新闻卡片
        function renderNews(news) {{
            const newsContainer = document.getElementById('newsContainer');
            newsContainer.innerHTML = '';

            news.forEach(item => {{
                const card = document.createElement('div');
                card.className = 'news-card';
                card.innerHTML = `
                    <h3 class="news-title">${{item.title}}</h3>
                    <p class="news-content">${{item.content}}</p>
                    <div class="news-meta">
                        <span class="news-time">${{item.time}}</span>
                        <span class="news-source">${{item.source}}</span>
                    </div>
                    <a href="${{item.link}}" class="news-link" target="_blank">阅读原文</a>
                `;
                newsContainer.appendChild(card);
            }});
        }}

        // 显示提示消息
        function showToast(message) {{
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 3000);
        }}

        // 分享功能
        function shareNews() {{
            let shareContent = '';
            newsData.forEach((item, index) => {{
                shareContent += `${{index + 1}}、${{item.title}}\\n`;
            }});
            shareContent += `\\n更多详情请见 https://harker1544525153-lang.github.io/ai-insights/`;

            // 使用现代Clipboard API复制内容
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(shareContent)
                    .then(() => {{
                        showToast('复制成功！');
                    }})
                    .catch(err => {{
                        console.error('复制失败:', err);
                        showToast('复制失败，请手动复制');
                    }});
            }} else {{
                // 兼容旧浏览器
                const textArea = document.createElement('textarea');
                textArea.value = shareContent;
                document.body.appendChild(textArea);
                textArea.select();
                try {{
                    document.execCommand('copy');
                    showToast('复制成功！');
                }} catch (err) {{
                    console.error('复制失败:', err);
                    showToast('复制失败，请手动复制');
                }}
                document.body.removeChild(textArea);
            }}
        }}

        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {{
            renderNews(newsData);

            // 绑定分享按钮事件
            document.getElementById('shareBtn').addEventListener('click', shareNews);

            // 绑定刷新按钮事件
            document.getElementById('refreshBtn').addEventListener('click', function() {{
                // 模拟刷新效果
                const newsContainer = document.getElementById('newsContainer');
                newsContainer.innerHTML = '<div class="loading">刷新中...</div>';
                setTimeout(() => {{
                    renderNews(newsData);
                }}, 1000);
            }});
        }});
    </script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    try:
        # 获取最新资讯
        news = fetch_news()
        # 生成HTML文件
        generate_html(news)
        print("资讯更新完成！")
    except Exception as e:
        print(f"执行出错：{e}")