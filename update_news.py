import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_news():
    """获取最新AI行业资讯"""
    news_data = []
    
    # 这里添加从各个数据源获取资讯的逻辑
    # 示例：从API或网页抓取最新资讯
    
    # 示例数据（实际应从真实数据源获取）
    news_data = [
        {
            "id": 1,
            "title": "英伟达发布2026财年Q4财报，日赚3.28亿美元",
            "content": "2026年2月27日，英伟达公布2026财年第四季度财报，Q4营收681.27亿美元，同比增长73%，全年营收2159.38亿美元，同比增长65%，净利润1200.67亿美元。黄仁勋宣布AI拐点已至。",
            "source": "英伟达",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "link": "https://example.com/news1"
        },
        {
            "id": 2,
            "title": "华为祭出AI编程利器，集成智谱、DeepSeek模型",
            "content": "华为云码道集成智谱GLM-5.0、DeepSeek-V3.2等模型，并持续增训，提供鸿蒙及昇腾专属模型，且支持自定义第三方模型接入。在智能体扩展方面，提供四层扩展机制。",
            "source": "华为",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "link": "https://example.com/news2"
        },
        # 更多资讯...
    ]
    
    return news_data

def generate_html(news):
    """生成HTML文件"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # HTML模板（与之前相同）
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日AI行业洞察·十大精选</title>
    <style>
        /* 样式代码与之前相同 */
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>每日AI行业洞察·十大精选 · {current_date}</h1>
            <!-- 按钮代码 -->
        </header>
        <div id="newsContainer" class="news-grid"></div>
        <footer>
            <p>最近更新：{current_time}</p>
        </footer>
    </div>
    <script>
        const newsData = {json.dumps(news, ensure_ascii=False)};
        // JavaScript代码与之前相同
    </script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == "__main__":
    try:
        print("开始获取最新资讯...")
        news = fetch_news()
        print(f"获取到 {len(news)} 条资讯")
        generate_html(news)
        print("资讯更新完成！")
    except Exception as e:
        print(f"执行出错：{e}")
        import traceback
        traceback.print_exc()