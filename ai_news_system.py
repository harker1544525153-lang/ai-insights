#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI简讯自动化系统
从AI_sources.xlsx获取数据源，生成简讯并保存到resultAI.xlsx
"""

import pandas as pd
import requests
import feedparser
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import os
from urllib.parse import urljoin
import json

class AINewsSystem:
    def __init__(self):
        self.sources_file = 'AI_sources.xlsx'
        self.results_file = 'resultAI.xlsx'
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
        try:
            df = pd.read_excel(self.sources_file)
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ 加载数据源失败: {e}")
            return []
    
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
            selectors = [
                'article',
                '.news-item',
                '.article',
                '.post',
                'h3 a',
                '.title a'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    for elem in elements[:5]:  # 只取前5条
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
    
    def extract_content(self, url):
        """提取文章内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取正文内容
            content_selectors = [
                'article',
                '.content',
                '.post-content',
                '.article-content',
                'main'
            ]
            
            content = ''
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text().strip()
                    break
            
            # 如果没找到特定选择器，尝试获取整个body
            if not content:
                content = soup.get_text().strip()
            
            # 清理内容
            content = re.sub(r'\s+', ' ', content)
            content = content[:2000]  # 限制长度
            
            return content, None
            
        except Exception as e:
            return '', f"内容提取失败: {e}"
    
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
    
    def generate_summary(self, content, title):
        """生成摘要（200-300字）"""
        if not content:
            return "内容获取失败，无法生成摘要"
        
        # 提取关键信息
        sentences = re.split(r'[.!?。！？]', content)
        key_sentences = []
        
        # 寻找包含关键信息的句子
        keywords = ['发布', '推出', '宣布', '合作', '投资', '融资', '增长', '下降', '达到', '超过']
        
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                key_sentences.append(sentence.strip())
        
        # 如果没找到关键词，使用前几个句子
        if not key_sentences:
            key_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 10]
        
        summary = ' '.join(key_sentences[:5])
        
        # 控制长度
        if len(summary) > 300:
            summary = summary[:297] + '...'
        elif len(summary) < 200:
            # 补充内容
            remaining = 200 - len(summary)
            additional = content[len(summary):len(summary)+remaining]
            summary += additional
        
        return summary
    
    def generate_comment(self, title, summary, category):
        """生成点评（2-3句话）"""
        # 根据类别生成不同的点评角度
        if category == '大模型':
            angles = [
                "从技术发展角度看，",
                "在AI模型竞争格局中，",
                "对行业技术标准的影响，"
            ]
        elif category == '云计算':
            angles = [
                "从云服务市场格局分析，",
                "对企业数字化转型的影响，",
                "在云计算技术演进中的意义，"
            ]
        else:  # 应用落地
            angles = [
                "从商业应用价值评估，",
                "对产业生态的影响，",
                "在技术商业化进程中的意义，"
            ]
        
        # 生成点评内容
        comments = []
        comments.append(f"{angles[0]}该事件反映了当前技术发展的主要趋势。")
        comments.append(f"{angles[1]}可能对相关企业的战略布局产生重要影响。")
        comments.append(f"{angles[2]}值得关注后续的市场反应和技术演进。")
        
        return ' '.join(comments[:2])  # 取前2句
    
    def is_recent_article(self, publish_time):
        """判断是否为近期文章"""
        if not publish_time:
            return False
        
        try:
            if isinstance(publish_time, str):
                # 尝试解析时间字符串
                time_formats = [
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                    '%a, %d %b %Y %H:%M:%S %z'
                ]
                
                article_date = None
                for fmt in time_formats:
                    try:
                        article_date = datetime.strptime(publish_time, fmt).date()
                        break
                    except:
                        continue
                
                if not article_date:
                    # 如果无法解析，假设是今天的文章
                    return True
                
                return article_date in [self.today, self.previous_workday]
            
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
        if rss_url and pd.notna(rss_url):
            articles, rss_error = self.fetch_rss_feed(rss_url)
            if rss_error:
                failure_reason = f"RSS获取失败: {rss_error}"
                print(f"   ❌ RSS失败: {rss_error}")
        
        # 如果RSS失败或没有RSS，使用网站爬取
        if not articles and home_url and pd.notna(home_url):
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
        for article in articles[:10]:  # 只处理前10条
            publish_time = article.get('published', article.get('updated', ''))
            
            if self.is_recent_article(publish_time):
                recent_articles.append(article)
        
        if not recent_articles:
            latest_time = articles[0].get('published', '') if articles else '无时间信息'
            return {
                'name': name,
                'articles_count': 0,
                'failure_reason': f"最新文章时间{latest_time}，不满足发布时间属于今日简讯今天及前一个工作日要求"
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
        
        for article in source_result['articles'][:3]:  # 每个源最多处理3条
            title = article.get('title', '')
            link = article.get('link', '')
            
            if not title or not link:
                continue
            
            # 提炼标题
            refined_title = self.refine_title(title)
            
            # 提取内容
            content, content_error = self.extract_content(link)
            
            # 生成摘要
            summary = self.generate_summary(content, refined_title)
            
            # 生成点评
            comment = self.generate_comment(refined_title, summary, source_result['category'])
            
            news_items.append({
                'title': refined_title,
                'original_title': title,
                'summary': summary,
                'comment': comment,
                'link': link,
                'source': source_result['name'],
                'category': source_result['category'],
                'publish_time': article.get('published', datetime.now().isoformat())
            })
            
            # 添加延迟避免被封
            time.sleep(1)
        
        return news_items
    
    def save_results(self, results):
        """保存结果到Excel"""
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
        
        # 创建DataFrame并保存
        df = pd.DataFrame(result_data)
        df.to_excel(self.results_file, index=False)
        
        print(f"✅ 结果已保存到: {self.results_file}")
    
    def generate_html(self, all_news):
        """生成HTML文件"""
        today_date = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
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
            font-size: 0.9rem;
            color: #6c757d;
            line-height: 1.5;
            margin-bottom: 8px;
        }}
        
        .insight-comment {{
            font-size: 0.85rem;
            color: #28a745;
            font-style: italic;
            background: #f0fff4;
            padding: 8px 10px;
            border-radius: 4px;
            border-left: 3px solid #28a745;
            margin-bottom: 8px;
        }}
        
        .insight-meta {{
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 0.8rem;
            color: #6c757d;
        }}
        
        .footer {{
            text-align: center;
            padding: 15px;
            color: #6c757d;
            font-size: 0.85rem;
            margin-top: 20px;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .navbar {{
                flex-direction: column;
                gap: 10px;
                align-items: stretch;
            }}
            
            .nav-controls {{
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }}
            
            .nav-controls select {{
                flex: 1;
                min-width: 120px;
            }}
            
            .preview-list {{
                gap: 4px;
            }}
            
            .preview-item {{
                gap: 6px;
            }}
            
            .insight-header {{
                flex-wrap: wrap;
                gap: 8px;
            }}
            
            .insight-title {{
                min-width: 100%;
                order: 1;
            }}
            
            .insight-category {{
                order: 2;
            }}
            
            .insight-source {{
                order: 3;
            }}
            
            .read-more {{
                order: 4;
            }}
            
            .insight-content {{
                margin-left: 0;
            }}
            
            .insight-meta {{
                flex-direction: column;
                gap: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 导航栏 -->
        <div class="navbar">
            <div class="nav-title">AI简讯</div>
            <div class="nav-controls">
                <select id="dateSelect">
                    <option value="{today_date}">今日简讯</option>
                    <option value="2026-03-10">2026-03-10</option>
                    <option value="2026-03-09">2026-03-09</option>
                </select>
                <select id="categoryFilter">
                    <option value="">所有分类</option>
                    <option value="大模型">大模型</option>
                    <option value="云计算">云计算</option>
                    <option value="应用落地">应用落地</option>
                </select>
                <button class="share-btn" onclick="shareAllTitles()">分享</button>
            </div>
        </div>
        
        <!-- 今日简讯预览 -->
        <div class="preview-section">
            <h3>今日简讯预览</h3>
            <div class="preview-list">
'''
        
        # 添加预览列表
        for i, news in enumerate(all_news, 1):
            html_content += f'''                <div class="preview-item">
                    <div class="preview-num">{i}</div>
                    <div class="preview-title">{news['title']}</div>
                </div>
'''
        
        html_content += f'''            </div>
        </div>
        
        <!-- 简讯列表 -->
        <div class="insights-section">
'''
        
        # 添加简讯列表
        for i, news in enumerate(all_news, 1):
            html_content += f'''            <div class="insight-item">
                <div class="insight-header">
                    <div class="insight-num">{i}</div>
                    <div class="insight-title">{news['title']}</div>
                    <div class="insight-category">{news['category']}</div>
                    <div class="insight-source">{news['source']}</div>
                    <a href="{news['link']}" class="read-more" target="_blank">阅读原文</a>
                </div>
                <div class="insight-content">
                    <div class="insight-summary">{news['summary']}</div>
                    <div class="insight-comment">{news['comment']}</div>
                    <div class="insight-meta">
                        <span>发布时间: {news['publish_time']}</span>
                        <span>来源: {news['source']}</span>
                    </div>
                </div>
            </div>
'''
        
        html_content += f'''        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>最近更新：{current_time}</p>
        </div>
    </div>
    
    <script>
        // 分享所有标题
        function shareAllTitles() {{
            const titles = document.querySelectorAll('.insight-title');
            let titleText = '';
            titles.forEach(function(title, index) {{
                titleText += (index + 1) + '. ' + title.textContent + '\\n';
            }});
            
            const shareText = '今日AI简讯标题预览：\\n' + titleText + '\\n更多详见：https://harker1544525153-lang.github.io/ai-insights/';
            
            // 复制到剪贴板
            navigator.clipboard.writeText(shareText).then(function() {{
                alert('标题已复制到剪贴板！');
            }}, function(err) {{
                console.error('复制失败: ', err);
            }});
        }}
        
        // 分类筛选
        document.getElementById('categoryFilter').addEventListener('change', function() {{
            const selectedCategory = this.value;
            const items = document.querySelectorAll('.insight-item');
            
            items.forEach(item => {{
                const category = item.querySelector('.insight-category').textContent;
                if (selectedCategory === '' || category === selectedCategory) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }});
        
        // 日期选择
        document.getElementById('dateSelect').addEventListener('change', function() {{
            const selectedDate = this.value;
            // 这里可以添加日期筛选逻辑
            alert('日期筛选功能待实现，当前显示：' + selectedDate);
        }});
    </script>
</body>
</html>'''
        
        # 写入HTML文件
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML文件生成完成: index.html")
    
    def run(self):
        """运行AI简讯系统"""
        print("🚀 开始AI简讯自动化系统...")
        print(f"📅 日期范围: {self.today} - {self.previous_workday}")
        
        # 加载数据源
        sources = self.load_sources()
        if not sources:
            print("❌ 没有找到数据源，请检查AI_sources.xlsx文件")
            return
        
        print(f"📊 加载了{len(sources)}个数据源")
        
        # 处理每个数据源
        results = []
        all_news = []
        
        for source in sources:
            result = self.process_source(source)
            results.append(result)
            
            # 如果处理成功，生成简讯内容
            if result.get('articles_count', 0) > 0:
                news_items = self.generate_news_content(result)
                all_news.extend(news_items)
        
        # 保存结果
        self.save_results(results)
        
        # 生成HTML文件
        if all_news:
            self.generate_html(all_news)
            print(f"📰 生成了{len(all_news)}条AI简讯")
        else:
            print("⚠️ 没有生成任何简讯内容")
        
        # 统计信息
        success_count = sum(1 for r in results if r.get('articles_count', 0) > 0)
        failure_count = len(results) - success_count
        
        print(f"\n📊 处理结果统计:")
        print(f"   ✅ 成功处理: {success_count}个数据源")
        print(f"   ❌ 处理失败: {failure_count}个数据源")
        print(f"   📄 生成简讯: {len(all_news)}条")
        print(f"   💾 结果文件: {self.results_file}")
        print(f"   🌐 HTML文件: index.html")
        
        print("\n✅ AI简讯系统执行完成！")

if __name__ == "__main__":
    system = AINewsSystem()
    system.run()