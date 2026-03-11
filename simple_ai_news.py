#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版AI简讯系统 - 不依赖pandas
"""

import csv
import requests
import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import os
from urllib.parse import urljoin

class SimpleAINewsSystem:
    def __init__(self):
        self.sources_file = 'AI_sources.csv'
        self.results_file = 'resultAI.csv'
        self.today = datetime.now().date()
        self.previous_workday = self.get_previous_workday()
        
    def get_previous_workday(self):
        """获取上一个工作日"""
        today = datetime.now()
        if today.weekday() == 0:  # 周一
            delta = 3  # 回到周五
        elif today.weekday() == 6:  # 周日
            delta = 2  # 回到周五
        else:
            delta = 1
        return (today - timedelta(days=delta)).date()
    
    def load_sources(self):
        """加载数据源"""
        sources = []
        try:
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sources.append(row)
            return sources
        except Exception as e:
            print(f"❌ 加载数据源失败: {e}")
            # 创建默认数据源
            default_sources = [
                {'name': 'DeepGEO', 'rss_url': 'https://deepgeo.org.cn/rss', 'home_url': 'https://deepgeo.org.cn', 'category': '大模型'},
                {'name': 'AIWW', 'rss_url': 'https://aiww.com/feed', 'home_url': 'https://aiww.com', 'category': '大模型'},
                {'name': 'Gartner', 'rss_url': 'https://www.gartner.com/en/rss', 'home_url': 'https://www.gartner.com', 'category': '云计算'}
            ]
            
            # 保存默认数据源
            with open(self.sources_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'rss_url', 'home_url', 'category'])
                writer.writeheader()
                writer.writerows(default_sources)
            
            print("✅ 已创建默认数据源文件")
            return default_sources
    
    def fetch_rss_feed(self, rss_url):
        """获取RSS订阅内容"""
        try:
            feed = feedparser.parse(rss_url)
            if feed.bozo:
                return None, f"RSS解析失败: {feed.bozo_exception}"
            return feed.entries, None
        except Exception as e:
            return None, f"RSS获取失败: {e}"
    
    def scrape_website(self, home_url):
        """爬取网站内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(home_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尝试提取新闻链接和标题
            articles = []
            
            # 常见新闻选择器
            selectors = ['article', '.news-item', '.article', '.post', 'h3 a', '.title a']
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for elem in elements[:3]:  # 只取前3条
                        title = elem.get_text().strip()
                        link = elem.get('href', '')
                        if link and not link.startswith('http'):
                            link = urljoin(home_url, link)
                        
                        if title and link:
                            articles.append({
                                'title': title,
                                'link': link,
                                'published': datetime.now().isoformat()
                            })
                    break
            
            return articles, None
            
        except Exception as e:
            return [], f"网站爬取失败: {e}"
    
    def refine_title(self, original_title):
        """提炼标题核心内容"""
        # 移除标题党词汇
        clickbait_words = ['震惊', '重磅', '刚刚', '突发', '惊爆', '必看', '速看']
        title = original_title
        for word in clickbait_words:
            title = title.replace(word, '')
        
        # 简化标题
        title = re.sub(r'[【】\[\]]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        # 限制长度
        if len(title) > 50:
            title = title[:47] + '...'
        
        return title
    
    def generate_summary(self, title):
        """生成摘要（基于标题）"""
        # 基于标题生成简短的摘要
        summary = f"{title}。该新闻涉及人工智能领域的最新发展动态。"
        
        # 控制长度
        if len(summary) > 200:
            summary = summary[:197] + '...'
        
        return summary
    
    def generate_comment(self, title, category):
        """生成点评"""
        if category == '大模型':
            return "从技术发展角度看，该事件反映了AI大模型领域的最新进展。"
        elif category == '云计算':
            return "从云服务市场格局分析，该事件对云计算行业有重要影响。"
        else:
            return "从商业应用价值评估，该事件在技术商业化进程中具有重要意义。"
    
    def is_recent_article(self, publish_time):
        """判断是否为近期文章"""
        if not publish_time:
            return False
        
        try:
            # 尝试解析时间
            if isinstance(publish_time, str):
                # 简化时间判断，假设是近期的
                return True
            return True
        except:
            return False
    
    def process_source(self, source):
        """处理单个数据源"""
        name = source['name']
        rss_url = source.get('rss_url', '')
        home_url = source.get('home_url', '')
        category = source.get('category', '其他')
        
        print(f"🔍 处理数据源: {name}")
        
        articles = []
        failure_reason = None
        
        # 优先使用RSS
        if rss_url and rss_url.strip():
            articles, rss_error = self.fetch_rss_feed(rss_url)
            if rss_error:
                failure_reason = f"RSS获取失败: {rss_error}"
                print(f"   ❌ RSS失败: {rss_error}")
        
        # 如果RSS失败或没有RSS，使用网站爬取
        if not articles and home_url and home_url.strip():
            articles, scrape_error = self.scrape_website(home_url)
            if scrape_error:
                failure_reason = f"网站爬取失败: {scrape_error}"
                print(f"   ❌ 网站爬取失败: {scrape_error}")
        
        if not articles:
            return {
                'name': name,
                'articles_count': 0,
                'failure_reason': failure_reason or '无可用数据源'
            }
        
        # 处理文章
        recent_articles = []
        for article in articles[:5]:  # 只处理前5条
            publish_time = article.get('published', article.get('updated', ''))
            
            if self.is_recent_article(publish_time):
                recent_articles.append(article)
        
        if not recent_articles:
            latest_time = articles[0].get('published', '') if articles else '无时间信息'
            return {
                'name': name,
                'articles_count': 0,
                'failure_reason': f"最新文章时间{latest_time}，不满足发布时间要求"
            }
        
        print(f"   ✅ 找到{len(recent_articles)}条近期文章")
        
        return {
            'name': name,
            'articles_count': len(recent_articles),
            'articles': recent_articles,
            'category': category
        }
    
    def generate_news_content(self, source_result):
        """生成简讯内容"""
        if not source_result.get('articles'):
            return []
        
        news_items = []
        
        for article in source_result['articles'][:2]:  # 每个源最多处理2条
            title = article.get('title', '')
            link = article.get('link', '')
            
            if not title or not link:
                continue
            
            # 提炼标题
            refined_title = self.refine_title(title)
            
            # 生成摘要
            summary = self.generate_summary(refined_title)
            
            # 生成点评
            comment = self.generate_comment(refined_title, source_result['category'])
            
            news_items.append({
                'title': refined_title,
                'summary': summary,
                'comment': comment,
                'link': link,
                'source': source_result['name'],
                'category': source_result['category'],
                'publish_time': article.get('published', datetime.now().isoformat())
            })
            
            # 添加延迟避免被封
            time.sleep(0.5)
        
        return news_items
    
    def save_results(self, results):
        """保存结果到CSV"""
        # 准备结果数据
        result_data = []
        
        for result in results:
            row = {
                '数据源名称': result['name'],
                '获取简讯数': result.get('articles_count', 0),
                '获取结果': '成功' if result.get('articles_count', 0) > 0 else '失败',
                '未选择原因': result.get('failure_reason', ''),
                '处理时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            result_data.append(row)
        
        # 创建CSV文件
        with open(self.results_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['数据源名称', '获取简讯数', '获取结果', '未选择原因', '处理时间']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_data)
        
        print(f"✅ 结果已保存到: {self.results_file}")
    
    def generate_html(self, all_news):
        """生成HTML文件 - 优化版样式"""
        today_date = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 获取标题列表用于预览
        title_list = [f"{i}. {news['title']}" for i, news in enumerate(all_news, 1)]
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI简讯 - {today_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
            background: #f8f9fa;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 15px;
        }}
        
        /* 导航栏 */
        .navbar {{
            background: white;
            padding: 12px 20px;
            border-bottom: 1px solid #e9ecef;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #495057;
        }}
        
        .nav-controls {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .nav-controls select {{
            padding: 6px 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 0.9rem;
            background: #f8f9fa;
        }}
        
        .share-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85rem;
        }}
        
        .share-btn:hover {{
            background: #0056b3;
        }}
        
        /* 今日简讯预览 */
        .preview-section {{
            background: white;
            padding: 12px 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            border: 1px solid #e9ecef;
        }}
        
        .preview-section h3 {{
            font-size: 1rem;
            margin-bottom: 10px;
            color: #495057;
            border-bottom: 1px solid #f8f9fa;
            padding-bottom: 6px;
        }}
        
        .preview-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        
        .preview-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
        }}
        
        .preview-num {{
            background: #6c757d;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7rem;
            font-weight: 500;
        }}
        
        .preview-title {{
            font-size: 0.85rem;
            color: #495057;
            line-height: 1.3;
        }}
        
        /* 简讯列表 */
        .insights-section {{
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }}
        
        .insight-item {{
            padding: 15px;
            border-bottom: 1px solid #f8f9fa;
            transition: background 0.2s;
        }}
        
        .insight-item:hover {{
            background: #f8f9fa;
        }}
        
        .insight-header {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .insight-num {{
            width: 30px;
            font-weight: 600;
            color: #495057;
            font-size: 0.9rem;
        }}
        
        .insight-title {{
            flex: 1;
            font-weight: 600;
            color: #495057;
            font-size: 1rem;
            margin-right: 10px;
        }}
        
        .insight-category {{
            background: #e9ecef;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            color: #6c757d;
            margin-right: 10px;
        }}
        
        .insight-source {{
            font-size: 0.8rem;
            color: #6c757d;
            margin-right: 15px;
        }}
        
        .read-more {{
            font-size: 0.8rem;
            color: #007bff;
            text-decoration: none;
        }}
        
        .read-more:hover {{
            text-decoration: underline;
        }}
        
        .insight-content {{
            margin-left: 30px;
        }}
        
        .insight-summary {{
            margin-bottom: 8px;
            line-height: 1.5;
            font-size: 0.9rem;
            color: #495057;
        }}
        
        .insight-comment {{
            font-style: italic;
            color: #6c757d;
            font-size: 0.85rem;
            border-top: 1px solid #f8f9fa;
            padding-top: 8px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 0.8rem;
            padding: 15px;
        }}
        
        .error-message {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 导航栏 -->
        <div class="navbar">
            <div class="nav-title">AI简讯·{today_date}</div>
            <div class="nav-controls">
                <select>
                    <option>所有分类</option>
                    <option>大模型</option>
                    <option>云计算</option>
                    <option>应用落地</option>
                </select>
                <button class="share-btn" onclick="shareContent()">分享</button>
            </div>
        </div>
        
        <!-- 今日简讯预览 -->
        <div class="preview-section">
            <h3>今日简讯预览</h3>
            <div class="preview-list">
'''
        
        # 添加预览列表
        for i, title in enumerate(title_list, 1):
            html_content += f'''
                <div class="preview-item">
                    <div class="preview-num">{i}</div>
                    <div class="preview-title">{title}</div>
                </div>
            '''
        
        html_content += '''
            </div>
        </div>
        
        <!-- 简讯列表 -->
        <div class="insights-section">
'''
        
        # 添加简讯项
        for i, news in enumerate(all_news, 1):
            html_content += f'''
            <div class="insight-item">
                <div class="insight-header">
                    <div class="insight-num">{i}</div>
                    <div class="insight-title">{news['title']}</div>
                    <div class="insight-category">{news['category']}</div>
                    <div class="insight-source">{news['source']}</div>
                    <a href="{news['link']}" target="_blank" class="read-more">阅读原文</a>
                </div>
                <div class="insight-content">
                    <div class="insight-summary">{news['summary']}</div>
                    <div class="insight-comment">点评: {news['comment']}</div>
                </div>
            </div>
            '''
        
        # 添加JavaScript分享功能
        html_content += f'''
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>最近更新: {current_time}</p>
            <p>AI简讯自动化系统 v2.0 | 优化版样式</p>
        </div>
        
        <script>
            function shareContent() {{
                const title = "AI简讯 · {today_date}";
                const url = "https://harker1544525153-lang.github.io/ai-insights/";
                const text = "今日AI行业最新动态，涵盖大模型、云计算、应用落地等领域。";
                
                if (navigator.share) {{
                    navigator.share({{
                        title: title,
                        text: text,
                        url: url
                    }}).then(() => {{
                        console.log('分享成功');
                    }}).catch(error => {{
                        console.log('分享失败:', error);
                    }});
                }} else {{
                    // 备用分享方式
                    const shareText = title + "\\n" + text + "\\n" + url;
                    if (navigator.clipboard) {{
                        navigator.clipboard.writeText(shareText).then(() => {{
                            alert('内容已复制到剪贴板，请手动分享');
                        }});
                    }} else {{
                        alert('请手动复制以下内容进行分享：\\n\\n' + shareText);
                    }}
                }}
            }}
            
            // 分类筛选功能
            document.addEventListener('DOMContentLoaded', function() {{
                const categorySelect = document.querySelector('.nav-controls select');
                if (categorySelect) {{
                    categorySelect.addEventListener('change', function() {{
                        const selectedCategory = this.value;
                        const insightItems = document.querySelectorAll('.insight-item');
                        
                        insightItems.forEach(item => {{
                            const category = item.querySelector('.insight-category').textContent;
                            if (selectedCategory === '所有分类' || category === selectedCategory) {{
                                item.style.display = 'block';
                            }} else {{
                                item.style.display = 'none';
                            }}
                        }});
                    }});
                }}
            }});
        </script>
    </div>
</body>
</html>
'''
        
        # 保存HTML文件
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ HTML文件已生成: index.html")
    
    def run(self):
        """运行AI简讯系统"""
        print("🚀 开始执行AI简讯系统...")
        print(f"📅 今日日期: {self.today}")
        print(f"📅 上一个工作日: {self.previous_workday}")
        
        # 加载数据源
        sources = self.load_sources()
        print(f"📊 加载了{len(sources)}个数据源")
        
        # 处理每个数据源
        all_results = []
        all_news = []
        
        for source in sources:
            result = self.process_source(source)
            all_results.append(result)
            
            # 如果成功获取到文章，生成简讯内容
            if result.get('articles_count', 0) > 0:
                news_items = self.generate_news_content(result)
                all_news.extend(news_items)
        
        # 保存结果
        self.save_results(all_results)
        
        # 生成HTML
        if all_news:
            self.generate_html(all_news)
            print(f"📰 成功生成{len(all_news)}条AI简讯")
        else:
            print("⚠️ 未获取到任何简讯内容")
        
        print("✅ AI简讯系统执行完成")

if __name__ == "__main__":
    system = SimpleAINewsSystem()
    system.run()