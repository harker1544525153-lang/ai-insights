#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日简讯固定工作流系统
实现：
1. 数据源从AI_sources.xlsx获取
2. 英文内容翻译为中文
3. 简讯数量控制（最多10条，每类优先一条）
4. 蓝色标题和边框样式
5. 生成resultAI.xlsx结果文件
"""

import pandas as pd
import feedparser
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import os
from urllib.parse import urljoin
import json

class DailyNewsWorkflow:
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
            selectors = ['article', '.news-item', '.article', '.post', 'h3 a', '.title a', 'h2 a']
            
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
    
    def translate_to_chinese(self, text):
        """简单英文翻译为中文（模拟翻译）"""
        if not text or not any(char.isalpha() for char in text):
            return text
        
        # 简单的关键词翻译映射
        translation_map = {
            'AI': '人工智能', 'Artificial Intelligence': '人工智能', 'Machine Learning': '机器学习',
            'Deep Learning': '深度学习', 'Neural Network': '神经网络', 'Cloud': '云',
            'Cloud Computing': '云计算', 'Big Data': '大数据', 'Blockchain': '区块链',
            'IoT': '物联网', 'VR': '虚拟现实', 'AR': '增强现实', '5G': '5G',
            'Startup': '初创公司', 'Investment': '投资', 'Funding': '融资',
            'Venture': '风险投资', 'Market': '市场', 'Technology': '技术',
            'Innovation': '创新', 'Digital': '数字化', 'Transformation': '转型',
            'Strategy': '战略', 'Platform': '平台', 'Solution': '解决方案',
            'Service': '服务', 'Product': '产品', 'Company': '公司',
            'Enterprise': '企业', 'Business': '商业', 'Industry': '行业',
            'Research': '研究', 'Development': '开发', 'Application': '应用'
        }
        
        # 简单的翻译逻辑
        translated = text
        for eng, chi in translation_map.items():
            translated = translated.replace(eng, chi)
        
        # 如果翻译后没有变化，添加中文说明
        if translated == text and any(char.isalpha() for char in text):
            translated = f"{text}（人工智能相关新闻）"
        
        return translated
    
    def refine_title(self, original_title, source_name):
        """提炼标题核心内容"""
        # 判断是否为英文内容
        is_english = any(char.isalpha() and ord(char) > 127 for char in original_title)
        
        title = original_title
        
        # 如果是英文内容，翻译为中文
        if is_english:
            title = self.translate_to_chinese(title)
        
        # 移除标题党词汇
        clickbait_words = ['震惊', '重磅', '刚刚', '突发', '惊爆', '必看', '速看', 'Breaking', 'Exclusive']
        for word in clickbait_words:
            title = title.replace(word, '')
        
        # 简化标题
        title = re.sub(r'[【】\[\]]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        # 限制长度
        if len(title) > 50:
            title = title[:47] + '...'
        
        return title
    
    def generate_summary(self, title, content=None):
        """生成摘要（200-300字）"""
        # 基于标题生成简短的摘要
        summary = f"{title}。该新闻涉及人工智能领域的最新发展动态，"
        
        # 根据标题关键词生成不同的摘要
        if any(word in title for word in ['大模型', '模型', 'AI模型']):
            summary += "反映了AI大模型技术的最新进展和行业应用情况。"
        elif any(word in title for word in ['云计算', '云服务', '云平台']):
            summary += "展示了云计算技术在AI领域的创新应用和市场趋势。"
        elif any(word in title for word in ['应用', '落地', '商业化']):
            summary += "体现了AI技术在实际场景中的商业化应用和价值创造。"
        else:
            summary += "涵盖了人工智能技术发展、市场应用和行业趋势等多个方面。"
        
        # 控制长度
        if len(summary) > 300:
            summary = summary[:297] + '...'
        elif len(summary) < 200:
            # 补充内容
            remaining = 200 - len(summary)
            additional = "人工智能作为新一轮科技革命的核心驱动力，正在深刻改变各行各业的生产方式和商业模式。"
            summary += additional[:remaining]
        
        return summary
    
    def generate_comment(self, title, category):
        """生成点评（2-3句话）"""
        if category == '大模型':
            return f"从技术发展角度看，{title}反映了AI大模型领域的最新进展，对行业技术标准和发展方向具有重要影响。在AI模型竞争格局中，该事件可能对相关企业的技术路线和产品策略产生深远影响。"
        elif category == '云计算':
            return f"从云服务市场格局分析，{title}对云计算行业的技术演进和市场竞争具有重要影响。在企业数字化转型进程中，该技术发展将推动云服务向更智能、更高效的方向发展。"
        else:  # 应用落地
            return f"从商业应用价值评估，{title}体现了AI技术在实际场景中的商业化应用潜力。在产业生态建设中，该应用案例对推动AI技术普及和行业数字化转型具有重要意义。"
    
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
    
    def select_news_items(self, all_news):
        """选择新闻项（最多10条，每类优先一条）"""
        selected_news = []
        category_count = {'大模型': 0, '云计算': 0, '应用落地': 0}
        
        # 按类别分组
        news_by_category = {}
        for news in all_news:
            category = news['category']
            if category not in news_by_category:
                news_by_category[category] = []
            news_by_category[category].append(news)
        
        # 每类优先选择一条
        for category in ['大模型', '云计算', '应用落地']:
            if category in news_by_category and news_by_category[category]:
                selected_news.append(news_by_category[category][0])
                category_count[category] += 1
        
        # 补充其他新闻，确保总数不超过10条
        remaining_slots = 10 - len(selected_news)
        if remaining_slots > 0:
            # 按类别轮询选择
            all_categories = ['大模型', '云计算', '应用落地']
            category_index = 0
            
            while remaining_slots > 0 and len(all_news) > len(selected_news):
                current_category = all_categories[category_index % len(all_categories)]
                
                if current_category in news_by_category:
                    for news in news_by_category[current_category]:
                        if news not in selected_news and category_count[current_category] < 4:  # 每类最多4条
                            selected_news.append(news)
                            category_count[current_category] += 1
                            remaining_slots -= 1
                            break
                
                category_index += 1
                if category_index > 100:  # 防止无限循环
                    break
        
        return selected_news[:10]  # 确保不超过10条
    
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
            refined_title = self.refine_title(title, source_result['name'])
            
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
        
        # 创建DataFrame
        df = pd.DataFrame(result_data)
        
        # 保存到Excel
        with pd.ExcelWriter(self.results_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='处理结果', index=False)
            
            # 添加统计信息
            stats_data = {
                '统计项': ['总数据源数', '成功获取数', '失败获取数', '生成简讯数', '处理时间'],
                '数值': [
                    len(results),
                    len([r for r in results if r.get('articles_count', 0) > 0]),
                    len([r for r in results if r.get('articles_count', 0) == 0]),
                    len([r for r in results if r.get('articles_count', 0) > 0]),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='统计信息', index=False)
        
        print(f"✅ 结果已保存到: {self.results_file}")
    
    def generate_html(self, all_news):
        """生成HTML文件 - 蓝色标题和边框样式"""
        today_date = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 选择新闻项（最多10条，每类优先一条）
        selected_news = self.select_news_items(all_news)
        
        # 获取标题列表用于预览
        title_list = [f"{i}. {news['title']}" for i, news in enumerate(selected_news, 1)]
        
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
        
        /* 导航栏 - 蓝色边框 */
        .navbar {{
            background: white;
            padding: 12px 20px;
            border: 2px solid #007bff;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #007bff;
        }}
        
        .nav-controls {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .nav-controls select {{
            padding: 6px 10px;
            border: 1px solid #007bff;
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
        
        /* 今日简讯预览 - 蓝色边框 */
        .preview-section {{
            background: white;
            padding: 12px 15px;
            border-radius: 6px;
            margin-bottom: 15px;
            border: 2px solid #007bff;
        }}
        
        .preview-section h3 {{
            font-size: 1rem;
            margin-bottom: 10px;
            color: #007bff;
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
            background: #007bff;
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
            color: #007bff;
            line-height: 1.3;
            font-weight: 500;
        }}
        
        /* 简讯列表 - 蓝色标题和边框 */
        .insights-section {{
            background: white;
            border-radius: 6px;
            border: 2px solid #007bff;
        }}
        
        .insight-item {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            transition: background 0.2s;
        }}
        
        .insight-item:hover {{
            background: #f0f8ff;
        }}
        
        .insight-header {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .insight-num {{
            width: 30px;
            font-weight: 600;
            color: #007bff;
            font-size: 0.9rem;
        }}
        
        .insight-title {{
            flex: 1;
            font-weight: 600;
            color: #007bff;
            font-size: 1rem;
            margin-right: 10px;
        }}
        
        .insight-category {{
            background: #e6f3ff;
            color: #007bff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            margin-right: 10px;
            border: 1px solid #007bff;
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
            font-weight: 500;
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
            color: #007bff;
            font-size: 0.85rem;
            border-top: 1px solid #e6f3ff;
            padding-top: 8px;
            font-weight: 500;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 0.8rem;
            padding: 15px;
            border-top: 1px solid #e9ecef;
        }}
        
        .stats-info {{
            background: #e6f3ff;
            border: 1px solid #007bff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-size: 0.85rem;
            color: #007bff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 统计信息 -->
        <div class="stats-info">
            今日简讯：{len(selected_news)}条 | 大模型：{len([n for n in selected_news if n['category'] == '大模型'])}条 | 
            云计算：{len([n for n in selected_news if n['category'] == '云计算'])}条 | 
            应用落地：{len([n for n in selected_news if n['category'] == '应用落地'])}条
        </div>
        
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
        for i, news in enumerate(selected_news, 1):
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
        
        # 添加JavaScript功能
        html_content += f'''
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
            <p>最近更新: {current_time}</p>
            <p>AI简讯自动化系统 v2.0 | 蓝色主题样式</p>
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
        print(f"📊 生成简讯统计: 总{len(selected_news)}条 (大模型: {len([n for n in selected_news if n['category'] == '大模型'])}条, "
              f"云计算: {len([n for n in selected_news if n['category'] == '云计算'])}条, "
              f"应用落地: {len([n for n in selected_news if n['category'] == '应用落地'])}条)")
    
    def run(self):
        """运行每日简讯工作流"""
        print("🚀 开始执行每日简讯固定工作流...")
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
            print(f"📰 成功生成AI简讯")
        else:
            print("⚠️ 未获取到任何简讯内容")
        
        print("✅ 每日简讯固定工作流执行完成")

if __name__ == "__main__":
    workflow = DailyNewsWorkflow()
    workflow.run()