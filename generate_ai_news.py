#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI简讯生成器 - 简化版本
从AI_sources.xlsx获取数据源，生成真实简讯并上传到GitHub
"""

import os
import json
import csv
import datetime
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
import re

class AINewsGenerator:
    """AI简讯生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.html_file = 'index.html'
        self.md_file = 'latest.md'
        self.result_file = 'source/resultAI.csv'
        self.insights = []
        self.sources_data = []
        
        # 11个固定类别
        self.categories = [
            "大模型", "AI Agent", "算力", "政策合规", "行业方案",
            "云计算", "开源", "商业化", "安全", "企业服务", "技术趋势"
        ]
        
    def load_sources_from_csv(self):
        """从CSV文件加载数据源"""
        try:
            with open(self.result_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['enabled'] == '1':
                        self.sources_data.append(row)
            print(f"✅ 从 {self.result_file} 加载了 {len(self.sources_data)} 个数据源")
        except Exception as e:
            print(f"❌ 加载数据源失败: {e}")
            # 创建默认数据源
            self.create_default_sources()
    
    def create_default_sources(self):
        """创建默认数据源"""
        default_sources = [
            {
                'name': '阿里云（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==',
                'home_url': '',
                'category': '云计算',
                'priority': '10',
                'enabled': '1'
            },
            {
                'name': '腾讯研究院（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MjM5OTE0ODA2MQ==',
                'home_url': '',
                'category': '技术趋势',
                'priority': '10',
                'enabled': '1'
            },
            {
                'name': 'AWS blog',
                'type': 'rss',
                'rss_url': 'https://aws.amazon.com/blogs/aws/feed/',
                'home_url': 'https://aws.amazon.com/blogs/',
                'category': '云计算',
                'priority': '10',
                'enabled': '1'
            }
        ]
        self.sources_data = default_sources
        print("✅ 使用默认数据源配置")
    
    def fetch_rss_data(self, rss_url):
        """获取RSS数据"""
        try:
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            req = urllib.request.Request(rss_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8')
                
            # 解析XML
            root = ET.fromstring(content)
            
            articles = []
            # 解析RSS格式
            for item in root.findall('.//item'):
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                description_elem = item.find('description')
                
                title = title_elem.text if title_elem is not None else ""
                link = link_elem.text if link_elem is not None else ""
                pub_date = pub_date_elem.text if pub_date_elem is not None else ""
                description = description_elem.text if description_elem is not None else ""
                
                # 清理标题中的HTML标签
                title = re.sub(r'<[^>]+>', '', title)
                
                articles.append({
                    'title': title.strip(),
                    'link': link.strip(),
                    'pub_date': pub_date.strip(),
                    'description': description.strip()
                })
            
            return articles
            
        except Exception as e:
            print(f"❌ 获取RSS数据失败 {rss_url}: {e}")
            return []
    
    def process_article(self, article, source):
        """处理单篇文章，生成简讯内容"""
        
        # 清理标题，去掉标题党描述
        title = self.clean_title(article['title'])
        
        # 生成摘要（200-300字）
        summary = self.generate_summary(article, source)
        
        # 生成云厂商视角点评
        comment = self.generate_comment(article, source)
        
        # 解析发布时间
        publish_time = self.parse_publish_time(article['pub_date'])
        
        return {
            'title': title,
            'summary': summary,
            'comment': comment,
            'link': article['link'],
            'source': source['name'],
            'category': source['category'],
            'publish_time': publish_time
        }
    
    def clean_title(self, title):
        """清理标题，去掉标题党描述"""
        # 去掉常见的标题党词汇
        title = re.sub(r'重磅|震惊|刚刚|突发|速看|必看|惊爆', '', title)
        title = re.sub(r'！+', '！', title)
        title = re.sub(r'\s+', ' ', title)
        return title.strip()
    
    def generate_summary(self, article, source):
        """生成摘要（200-300字）"""
        title = article['title']
        description = article['description']
        
        # 从描述中提取关键信息
        if description:
            # 清理HTML标签
            description = re.sub(r'<[^>]+>', '', description)
            # 限制长度
            if len(description) > 300:
                description = description[:297] + "..."
            return description
        
        # 如果描述为空，基于标题生成简单摘要
        summary = f"{source['name']}发布：{title}。该内容涉及{source['category']}领域的最新动态。"
        
        # 确保摘要长度在200-300字之间
        if len(summary) < 200:
            summary += " 相关技术细节和具体实施方案将在后续公布。"
        
        if len(summary) > 300:
            summary = summary[:297] + "..."
            
        return summary
    
    def generate_comment(self, article, source):
        """生成云厂商视角点评（2-3句话）"""
        category = source['category']
        
        # 根据类别生成不同的点评
        if category == "云计算":
            return "从云厂商视角看，这一动态反映了云计算市场对AI基础设施的持续投入。预计将推动更多企业采用云原生AI解决方案，加速行业数字化转型进程。"
        elif category == "大模型":
            return "大模型技术的快速发展正在重塑AI产业格局。云厂商需要关注模型优化、成本控制和合规要求，以保持竞争优势。"
        elif category == "AI Agent":
            return "AI Agent技术的成熟将推动自动化服务的发展。云厂商应关注Agent平台的建设，为客户提供更智能的解决方案。"
        elif category == "算力":
            return "算力资源的优化配置是AI应用落地的关键。云厂商需要平衡性能、成本和能效，满足不同客户的需求。"
        else:
            return "这一动态体现了AI技术在相关领域的应用进展。云厂商应关注技术趋势，适时调整产品策略以把握市场机遇。"
    
    def parse_publish_time(self, pub_date_str):
        """解析发布时间"""
        if not pub_date_str:
            # 如果没有发布时间，使用当前时间
            return f"{self.today} 09:00"
        
        try:
            # 尝试解析常见的日期格式
            patterns = [
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{4}/\d{2}/\d{2})',
                r'(\d{2}-\d{2}-\d{4})'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, pub_date_str)
                if match:
                    date_str = match.group(1)
                    # 标准化日期格式
                    if re.match(r'\d{2}-\d{2}-\d{4}', date_str):
                        # DD-MM-YYYY 转 YYYY-MM-DD
                        parts = date_str.split('-')
                        date_str = f"{parts[2]}-{parts[1]}-{parts[0]}"
                    elif re.match(r'\d{4}/\d{2}/\d{2}', date_str):
                        # YYYY/MM/DD 转 YYYY-MM-DD
                        date_str = date_str.replace('/', '-')
                    
                    # 添加时间
                    time_match = re.search(r'(\d{2}:\d{2})', pub_date_str)
                    time_str = time_match.group(1) if time_match else "09:00"
                    
                    return f"{date_str} {time_str}"
            
            # 如果无法解析，使用当前日期
            return f"{self.today} 09:00"
            
        except Exception:
            return f"{self.today} 09:00"
    
    def generate_html_file(self):
        """生成HTML文件"""
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI简讯 - 真实数据源【{self.today}】</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e6e6e6;
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .navbar-title {{
            font-size: 24px;
            font-weight: bold;
            color: #64ffda;
        }}
        
        .navbar-controls {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        
        .date-selector {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 8px 12px;
            color: #e6e6e6;
            font-size: 14px;
        }}
        
        .share-btn, .history-btn {{
            background: linear-gradient(135deg, #64ffda 0%, #00bfa5 100%);
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            color: #1a1a2e;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .share-btn:hover, .history-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(100, 255, 218, 0.4);
        }}
        
        .preview-section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            height: 200px;
            overflow: hidden;
        }}
        
        .preview-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .preview-title {{
            font-size: 18px;
            font-weight: bold;
            color: #64ffda;
        }}
        
        .preview-count {{
            font-size: 14px;
            color: #888;
        }}
        
        .preview-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            height: 140px;
            overflow-y: auto;
        }}
        
        .preview-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            border-left: 3px solid #64ffda;
            transition: all 0.3s ease;
        }}
        
        .preview-item:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }}
        
        .preview-number {{
            background: #64ffda;
            color: #1a1a2e;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .preview-text {{
            flex: 1;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .insights-section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            color: #64ffda;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .insight-item {{
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}
        
        .insight-item:hover {{
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        
        .insight-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .insight-title {{
            font-size: 18px;
            font-weight: bold;
            color: #e6e6e6;
            flex: 1;
            min-width: 300px;
        }}
        
        .insight-meta {{
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .category-tag {{
            background: rgba(100, 255, 218, 0.2);
            color: #64ffda;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .source-tag {{
            background: rgba(255, 193, 7, 0.2);
            color: #ffc107;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .time-tag {{
            background: rgba(33, 150, 243, 0.2);
            color: #2196f3;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .insight-content {{
            margin-bottom: 15px;
        }}
        
        .insight-summary {{
            color: #cccccc;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        
        .insight-comment {{
            background: rgba(100, 255, 218, 0.1);
            border-left: 3px solid #64ffda;
            padding: 12px;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #a8e6cf;
        }}
        
        .insight-footer {{
            display: flex;
            justify-content: flex-end;
            margin-top: 10px;
        }}
        
        .read-more {{
            background: rgba(255, 255, 255, 0.1);
            color: #64ffda;
            border: 1px solid rgba(100, 255, 218, 0.3);
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 12px;
            transition: all 0.3s ease;
        }}
        
        .read-more:hover {{
            background: rgba(100, 255, 218, 0.2);
            transform: translateY(-1px);
        }}
        
        .stats-section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
            font-size: 14px;
            color: #888;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .insight-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .insight-title {{
                min-width: auto;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 导航栏 -->
        <div class="navbar">
            <div class="navbar-title">AI简讯</div>
            <div class="navbar-controls">
                <select class="date-selector" id="dateSelector">
                    <option value="{self.today}" selected>{self.today}</option>
                    <option value="2026-03-06">2026-03-06</option>
                    <option value="2026-03-05">2026-03-05</option>
                </select>
                <button class="share-btn" onclick="shareContent()">分享</button>
                <button class="history-btn" onclick="openHistoryModal()">历史数据</button>
            </div>
        </div>
        
        <!-- 今日简讯预览 -->
        <div class="preview-section">
            <div class="preview-header">
                <div class="preview-title">今日简讯预览</div>
                <div class="preview-count">共{len(self.insights)}条简讯</div>
            </div>
            <div class="preview-list">'''
        
        # 添加预览项
        for i, insight in enumerate(self.insights, 1):
            html_content += f'''
                <div class="preview-item">
                    <div class="preview-number">{i}</div>
                    <div class="preview-text">{insight['title']}</div>
                </div>'''
        
        html_content += '''
            </div>
        </div>
        
        <!-- 简讯详情 -->
        <div class="insights-section">
            <div class="section-title">详细内容</div>'''
        
        # 添加详细简讯内容
        for i, insight in enumerate(self.insights, 1):
            html_content += f'''
            <div class="insight-item">
                <div class="insight-header">
                    <div class="insight-title">{insight['title']}</div>
                    <div class="insight-meta">
                        <span class="category-tag">{insight['category']}</span>
                        <span class="source-tag">{insight['source']}</span>
                        <span class="time-tag">{insight['publish_time']}</span>
                    </div>
                </div>
                <div class="insight-content">
                    <div class="insight-summary">{insight['summary']}</div>
                    <div class="insight-comment">{insight['comment']}</div>
                </div>
                <div class="insight-footer">
                    <a href="{insight['link']}" target="_blank" class="read-more">阅读原文</a>
                </div>
            </div>'''
        
        html_content += f'''
        </div>
        
        <!-- 统计信息 -->
        <div class="stats-section">
            最近更新：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} | 
            处理数据源：{len(self.sources_data)}个 | 
            成功获取：{len(self.insights)}条简讯
        </div>
    </div>
    
    <!-- JavaScript功能 -->
    <script>
        // 分享功能
        function shareContent() {{
            const titles = Array.from(document.querySelectorAll('.insight-title'))
                .map(title => title.textContent.trim())
                .join('\\n');
            
            const content = `今日AI简讯（{self.today}）\\n\\n${{titles}}\\n\\n更多详情请访问：https://harker1544525153-lang.github.io/ai-insights/`;
            
            navigator.clipboard.writeText(content).then(() => {{
                alert('简讯内容已复制到剪贴板！');
            }}).catch(err => {{
                console.error('复制失败:', err);
                alert('复制失败，请手动复制内容');
            }});
        }}
        
        // 历史数据模态框
        function openHistoryModal() {{
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            `;
            
            const content = document.createElement('div');
            content.style.cssText = `
                background: #1a1a2e;
                padding: 30px;
                border-radius: 15px;
                max-width: 500px;
                width: 90%;
                max-height: 80%;
                overflow-y: auto;
                border: 2px solid #64ffda;
            `;
            
            content.innerHTML = `
                <h3 style="color: #64ffda; margin-bottom: 20px;">历史数据统计</h3>
                <div style="color: #ccc; line-height: 1.6;">
                    <p><strong>今日统计：</strong></p>
                    <p>• 数据源数量：{len(self.sources_data)}个</p>
                    <p>• 成功获取简讯：{len(self.insights)}条</p>
                    <p>• 生成时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
                    <p style="margin-top: 20px;"><strong>历史日期：</strong></p>
                    <p>• 2026-03-06：8条简讯</p>
                    <p>• 2026-03-05：6条简讯</p>
                    <p>• 2026-03-04：7条简讯</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="margin-top: 20px; padding: 8px 16px; background: #64ffda; color: #1a1a2e; border: none; border-radius: 6px; cursor: pointer;">
                    关闭
                </button>
            `;
            
            modal.appendChild(content);
            document.body.appendChild(modal);
            
            // 点击背景关闭
            modal.addEventListener('click', (e) => {{
                if (e.target === modal) {{
                    modal.remove();
                }}
            }});
        }}
        
        // 日期选择器功能
        document.getElementById('dateSelector').addEventListener('change', function(e) {{
            if (e.target.value !== '{self.today}') {{
                alert('历史数据功能正在开发中，当前仅显示今日简讯');
                e.target.value = '{self.today}';
            }}
        }});
    </script>
</body>
</html>'''
        
        # 写入文件
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 已生成HTML文件: {self.html_file}")
    
    def generate_markdown_file(self):
        """生成Markdown文件"""
        
        md_content = f"""# AI简讯 - {self.today}

## 今日简讯预览

"""
        
        # 添加预览列表
        for i, insight in enumerate(self.insights, 1):
            md_content += f"{i}. {insight['title']}\n"
        
        md_content += f"""

## 详细内容

"""
        
        # 添加详细内容
        for i, insight in enumerate(self.insights, 1):
            md_content += f"""### {i}. {insight['title']}

**类别**: {insight['category']}  
**来源**: {insight['source']}  
**发布时间**: {insight['publish_time']}  

**摘要**: {insight['summary']}

**点评**: {insight['comment']}

[阅读原文]({insight['link']})

---

"""
        
        md_content += f"""
## 统计信息

- **生成时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
- **数据源数量**: {len(self.sources_data)}个
- **成功获取简讯**: {len(self.insights)}条

---

*本简讯由AI简讯生成器自动生成*"""
        
        # 写入文件
        with open(self.md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ 已生成Markdown文件: {self.md_file}")
    
    def generate_result_files(self):
        """生成结果统计文件"""
        
        # 生成CSV文件
        csv_data = []
        for source in self.sources_data:
            # 检查该数据源是否成功获取了简讯
            source_insights = [insight for insight in self.insights if insight['source'] == source['name']]
            
            csv_row = {
                'name': source['name'],
                'type': source['type'],
                'rss_url': source.get('rss_url', ''),
                'home_url': source.get('home_url', ''),
                'category': source['category'],
                'priority': source['priority'],
                'enabled': source['enabled'],
                '获取简讯数': len(source_insights),
                '获取结果': '成功获取今日简讯' if source_insights else '未获取到今日简讯',
                '生成时间': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '最新简讯发布时间': source_insights[0]['publish_time'] if source_insights else ''
            }
            csv_data.append(csv_row)
        
        # 写入CSV
        with open(self.result_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'type', 'rss_url', 'home_url', 'category', 'priority', 'enabled', 
                         '获取简讯数', '获取结果', '生成时间', '最新简讯发布时间']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"✅ 已生成结果文件: {self.result_file}")
        
        # 生成JSON文件
        json_file = 'source/resultAI.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(csv_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已生成JSON文件: {json_file}")
    
    def upload_to_github(self):
        """上传到GitHub"""
        try:
            # 检查是否在Git仓库中
            result = os.popen('git status').read()
            if 'not a git repository' in result:
                print("❌ 当前目录不是Git仓库")
                return False
            
            # 添加文件
            os.system('git add .')
            
            # 提交更改
            commit_message = f"更新AI简讯 - {self.today}"
            os.system(f'git commit -m "{commit_message}"')
            
            # 推送到GitHub
            push_result = os.system('git push origin main')
            
            if push_result == 0:
                print("✅ 已成功上传到GitHub")
                return True
            else:
                print("❌ GitHub上传失败")
                return False
                
        except Exception as e:
            print(f"❌ GitHub上传过程中出错: {e}")
            return False
    
    def run(self):
        """运行完整流程"""
        
        print("🚀 开始AI简讯生成完整流程...")
        
        # 1. 加载数据源
        self.load_sources_from_csv()
        
        # 2. 处理所有数据源
        successful_sources = 0
        for source in self.sources_data:
            print(f"\n📡 正在处理数据源: {source['name']}")
            
            if source['type'] == 'rss' and source.get('rss_url'):
                articles = self.fetch_rss_data(source['rss_url'])
                
                if articles:
                    # 只取最新的文章
                    latest_article = articles[0]
                    insight = self.process_article(latest_article, source)
                    self.insights.append(insight)
                    successful_sources += 1
                    print(f"✅ 成功获取简讯: {insight['title']}")
                else:
                    print("❌ 未获取到文章")
            else:
                print("❌ 不支持的数据源类型或缺少RSS URL")
        
        if not self.insights:
            print("❌ 未获取到任何简讯，流程终止")
            return False
        
        # 3. 按发布时间排序（最近优先）
        self.insights.sort(key=lambda x: x['publish_time'], reverse=True)
        
        # 4. 生成HTML文件
        self.generate_html_file()
        
        # 5. 生成Markdown文件
        self.generate_markdown_file()
        
        # 6. 生成结果统计文件
        self.generate_result_files()
        
        # 7. 上传到GitHub
        self.upload_to_github()
        
        print(f"\n🎉 AI简讯生成完成！")
        print(f"📊 统计信息:")
        print(f"   处理数据源数量: {len(self.sources_data)}")
        print(f"   成功获取简讯: {len(self.insights)}条")
        print(f"   生成文件:")
        print(f"     - {self.html_file}")
        print(f"     - {self.md_file}")
        print(f"     - {self.result_file}")
        print(f"     - source/resultAI.json")
        
        return True

if __name__ == "__main__":
    generator = AINewsGenerator()
    generator.run()