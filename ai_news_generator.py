#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI简讯生成器 - 从AI数据源获取并生成今日最新简讯
"""

import csv
import json
import os
from datetime import datetime
import feedparser
import time

class AINewsGenerator:
    """AI简讯生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.html_file = 'index.html'
        self.md_file = 'latest.md'
        self.result_file = 'source/resultAI.csv'
        self.insights = []
        self.sources_data = []
        
    def load_ai_sources(self):
        """加载AI数据源配置"""
        return [
            {
                'name': '阿里云（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==',
                'category': '云计算',
                'priority': 10,
                'enabled': 1
            },
            {
                'name': '腾讯研究院（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MjM5OTE0ODA2MQ==',
                'category': '技术趋势',
                'priority': 10,
                'enabled': 1
            },
            {
                'name': 'AWS blog',
                'type': 'rss',
                'rss_url': 'https://aws.amazon.com/blogs/aws/feed/',
                'category': '云计算',
                'priority': 10,
                'enabled': 1
            }
        ]
    
    def fetch_rss_data(self, rss_url, source_name):
        """从RSS源获取数据"""
        try:
            print(f"📡 正在从 {source_name} 获取RSS数据...")
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                return [], "RSS源无内容"
            
            articles = []
            for entry in feed.entries[:3]:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', '')
                }
                articles.append(article)
            
            return articles, "成功获取RSS数据"
            
        except Exception as e:
            print(f"❌ 获取RSS数据失败: {e}")
            return [], f"RSS获取失败: {str(e)}"
    
    def generate_insight_content(self, article, source_config):
        """生成简讯内容"""
        
        title = article['title']
        link = article['link']
        
        # 简化的内容生成逻辑
        if "阿里云" in source_config['name']:
            summary = f"{source_config['name']}发布最新动态：{title}。该动态涉及云计算服务优化和用户体验提升。"
            comment = "阿里云持续优化云服务体验，反映了市场对高质量AI基础设施的需求增长。"
        elif "腾讯" in source_config['name']:
            summary = f"{source_config['name']}发布研究报告：{title}。报告分析了AI行业发展趋势和市场前景。"
            comment = "腾讯研究院的报告为行业提供了有价值的参考，AI Agent市场前景广阔。"
        else:
            summary = f"{source_config['name']}发布技术更新：{title}。该更新涉及AI基础设施和计算能力提升。"
            comment = "技术更新推动AI应用发展，云厂商需要持续优化基础设施。"
        
        publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        return {
            'title': title,
            'category': source_config['category'],
            'source': source_config['name'],
            'publish_time': publish_time,
            'summary': summary,
            'comment': comment,
            'link': link
        }
    
    def process_all_sources(self):
        """处理所有数据源"""
        
        print("🚀 开始处理所有数据源...")
        
        sources_config = self.load_ai_sources()
        
        for source in sources_config:
            if not source.get('enabled', 1):
                print(f"⏭️  跳过禁用数据源: {source['name']}")
                continue
            
            print(f"\n📊 处理数据源: {source['name']}")
            
            insights_count = 0
            result_status = ""
            
            try:
                if source['type'] == 'rss' and source.get('rss_url'):
                    articles, status = self.fetch_rss_data(source['rss_url'], source['name'])
                    
                    if articles:
                        for article in articles:
                            insight = self.generate_insight_content(article, source)
                            self.insights.append(insight)
                            insights_count += 1
                        result_status = f"成功获取{insights_count}条简讯"
                    else:
                        result_status = status
                else:
                    result_status = "不支持的数据源类型"
                    
            except Exception as e:
                result_status = f"处理失败: {str(e)}"
                print(f"❌ 处理数据源失败: {source['name']} - {e}")
            
            # 记录数据源处理结果
            self.sources_data.append({
                'name': source['name'],
                'type': source.get('type', 'rss'),
                'rss_url': source.get('rss_url', ''),
                'category': source.get('category', '其他'),
                'priority': source.get('priority', 1),
                'enabled': source.get('enabled', 1),
                '获取简讯数': insights_count,
                '获取结果': result_status,
                '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            time.sleep(1)
    
    def generate_html_file(self):
        """生成HTML文件"""
        
        print("🔧 生成HTML文件...")
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # 构建HTML内容
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI简讯 - 真实数据源【{current_date}】</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{ 
            font-family: 'Microsoft YaHei', Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #f5f5f5; 
            line-height: 1.6;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
        }}
        
        /* 导航栏 */
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #007bff;
        }}
        .navbar-title {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .navbar-controls {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        .date-selector {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        .share-btn, .history-btn {{
            padding: 8px 16px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        .share-btn:hover, .history-btn:hover {{
            background: #0056b3;
        }}
        
        /* 今日简讯预览 */
        .preview-section {{
            margin-bottom: 30px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }}
        .preview-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .preview-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        .preview-count {{
            font-size: 14px;
            color: #666;
        }}
        .preview-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-height: 200px;
            overflow: hidden;
        }}
        .preview-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px;
            background: white;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }}
        .preview-number {{
            font-size: 14px;
            color: #007bff;
            font-weight: bold;
            min-width: 20px;
        }}
        .preview-text {{
            flex: 1;
            font-size: 14px;
            color: #333;
        }}
        .preview-category {{
            font-size: 12px;
            color: #666;
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        /* 简讯详情 */
        .insights-section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 2px solid #007bff;
        }}
        .insight {{
            margin-bottom: 25px;
            padding: 20px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .insight-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .insight-title {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
            flex: 1;
        }}
        .insight-link {{
            margin-left: 15px;
        }}
        .read-link {{
            color: #007bff;
            text-decoration: none;
            font-size: 14px;
            padding: 4px 8px;
            border: 1px solid #007bff;
            border-radius: 3px;
        }}
        .read-link:hover {{
            background: #007bff;
            color: white;
        }}
        .insight-meta {{
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        .insight-summary {{
            font-size: 15px;
            line-height: 1.6;
            color: #444;
            margin-bottom: 15px;
        }}
        .insight-comment {{
            font-size: 14px;
            line-height: 1.5;
            color: #666;
            padding: 12px;
            background: #f8f9fa;
            border-left: 3px solid #28a745;
            border-radius: 3px;
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .navbar {{
                flex-direction: column;
                gap: 15px;
            }}
            .navbar-controls {{
                width: 100%;
                justify-content: space-between;
            }}
            .preview-item {{
                flex-direction: column;
                align-items: flex-start;
                gap: 5px;
            }}
            .insight-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .insight-link {{
                margin-left: 0;
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
                    <option value="{current_date}" selected>{current_date}</option>
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
            <div class="preview-list">
'''
        
        # 添加预览项
        for i, insight in enumerate(self.insights, 1):
            html_content += f'''
                <div class="preview-item">
                    <div class="preview-number">{i}</div>
                    <div class="preview-text">{insight['title']}</div>
                    <div class="preview-category">{insight['category']}</div>
                </div>
'''
        
        html_content += '''
            </div>
        </div>
        
        <!-- 简讯详情 -->
        <div class="insights-section">
            <div class="section-title">详细内容</div>
'''
        
        # 添加详细简讯
        for i, insight in enumerate(self.insights, 1):
            html_content += f'''
            <div class="insight">
                <div class="insight-header">
                    <div class="insight-title">{i}、{insight['title']}</div>
                    <div class="insight-link">
                        <a href="{insight['link']}" target="_blank" class="read-link">阅读原文</a>
                    </div>
                </div>
                <div class="insight-meta">
                    分类：{insight['category']} | 来源：{insight['source']} | 发布时间：{insight['publish_time']}
                </div>
                <div class="insight-summary">
                    {insight['summary']}
                </div>
                <div class="insight-comment">
                    {insight['comment']}
                </div>
            </div>
'''
        
        html_content += '''
        </div>
    </div>
    
    <script>
        // 分享功能
        function shareContent() {
            const titles = [
'''
        
        # 添加分享标题（简化版，避免转义问题）
        for i, insight in enumerate(self.insights, 1):
            title = insight['title'].replace('"', '')
            html_content += f'                "{i}. {title}",\n'
        
        html_content += '''            ];
            
            const shareText = titles.join('\\n') + '\\n\\n更多详情请访问：' + window.location.href;
            
            // 复制到剪贴板
            navigator.clipboard.writeText(shareText).then(function() {
                showToast('内容已复制到剪贴板！');
            }).catch(function(err) {
                // 备用方法
                const textArea = document.createElement('textarea');
                textArea.value = shareText;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('内容已复制到剪贴板！');
            });
        }
        
        // 消息提示
        function showToast(message) {
            const toast = document.createElement('div');
            toast.textContent = message;
            toast.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #28a745; color: white; padding: 10px 20px; border-radius: 4px; z-index: 1001;';
            document.body.appendChild(toast);
            
            setTimeout(function() {
                document.body.removeChild(toast);
            }, 3000);
        }
        
        // 日期选择器事件
        document.getElementById('dateSelector').addEventListener('change', function() {
            const selectedDate = this.value;
            if (selectedDate !== ''' + f'"{current_date}"' + ''') {
                showToast('历史数据查看功能正在开发中...');
                this.value = ''' + f'"{current_date}"' + ''; // 重置为当前日期
            }
        });
        
        // 历史数据功能（简化版）
        function openHistoryModal() {
            showToast('历史数据查看功能正在开发中...');
        }
    </script>
</body>
</html>'''
        
        # 写入HTML文件
        with open(self.html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML文件已生成: {self.html_file}")
    
    def generate_markdown_file(self):
        """生成Markdown文件"""
        
        print("🔧 生成Markdown文件...")
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        md_content = f"""# AI简讯【{current_date}】

## 今日简讯概览（基于AI数据源）

"""
        
        # 添加简讯概览
        for i, insight in enumerate(self.insights, 1):
            md_content += f"{i}. **{insight['title']}** - {insight['category']} - {insight['publish_time']}\n"
        
        md_content += "\n---\n\n## 详细内容\n\n"
        
        # 添加详细内容
        for i, insight in enumerate(self.insights, 1):
            md_content += f"""### {i}、{insight['title']}
**分类：** {insight['category']}  
**来源：** {insight['source']}  
**发布时间：** {insight['publish_time']}  

**摘要：** {insight['summary']}

**点评：** {insight['comment']}

**原文链接：** {insight['link']}

---

"""
        
        # 写入Markdown文件
        with open(self.md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Markdown文件已生成: {self.md_file}")
    
    def generate_result_files(self):
        """生成结果统计文件"""
        
        print("🔧 生成数据源统计文件...")
        
        # 确保目录存在
        os.makedirs('source', exist_ok=True)
        
        # 定义表头
        headers = ['name', 'type', 'rss_url', 'category', 'priority', 'enabled', 
                  '获取简讯数', '获取结果', '生成时间']
        
        # 按优先级排序
        sorted_data = sorted(self.sources_data, key=lambda x: x.get('priority', 1), reverse=True)
        
        # 保存为CSV文件
        with open(self.result_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            for record in sorted_data:
                row = {}
                for header in headers:
                    row[header] = record.get(header, '')
                writer.writerow(row)
        
        print(f"✅ 数据源统计文件已生成: {self.result_file}")
        
        # 同时保存为JSON格式便于查看
        with open('source/resultAI.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(sorted_data, jsonfile, ensure_ascii=False, indent=2)
        
        print("✅ JSON格式文件已生成: source/resultAI.json")
    
    def upload_to_github(self):
        """上传到GitHub"""
        
        print("🚀 准备上传到GitHub...")
        
        try:
            import subprocess
            
            # 添加文件到Git
            subprocess.run(['git', 'add', 'index.html', 'latest.md', 'source/resultAI.csv', 'source/resultAI.json'], check=True)
            
            # 提交更改
            current_date = datetime.now().strftime('%Y-%m-%d')
            commit_message = f"自动更新AI简讯 {current_date}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # 推送到远程
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            print("✅ 成功上传到GitHub")
            
        except Exception as e:
            print(f"❌ GitHub上传失败: {e}")
            print("⚠️ 请手动执行以下命令上传：")
            print("git add index.html latest.md source/resultAI.csv source/resultAI.json")
            print("git commit -m '自动更新AI简讯'")
            print("git push origin main")
    
    def run(self):
        """运行完整流程"""
        
        print("🚀 开始AI简讯生成完整流程...")
        
        # 1. 处理所有数据源
        self.process_all_sources()
        
        if not self.insights:
            print("❌ 未获取到任何简讯，流程终止")
            return False
        
        # 2. 生成HTML文件
        self.generate_html_file()
        
        # 3. 生成Markdown文件
        self.generate_markdown_file()
        
        # 4. 生成结果统计文件
        self.generate_result_files()
        
        # 5. 上传到GitHub
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

def main():
    """主函数"""
    
    generator = AINewsGenerator()
    generator.run()

if __name__ == "__main__":
    main()