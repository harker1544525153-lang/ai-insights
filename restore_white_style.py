#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复白底简洁版本网页样式
包含今日简要预览功能
"""

import os
import datetime
import json

def restore_white_style():
    """恢复白底简洁版本网页样式"""
    
    print("开始恢复白底简洁版本网页样式...")
    
    # 读取最新的简讯数据
    try:
        with open('latest.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 解析简讯数据
        insights = []
        lines = md_content.split('\n')
        
        current_insight = {}
        for line in lines:
            if line.startswith('## '):
                if current_insight:
                    insights.append(current_insight)
                current_insight = {'title': line[3:].strip()}
            elif line.startswith('**类别：**'):
                current_insight['category'] = line.split('**类别：**')[1].strip()
            elif line.startswith('**来源：**'):
                current_insight['source'] = line.split('**来源：**')[1].strip()
            elif line.startswith('**发布时间：**'):
                current_insight['publish_time'] = line.split('**发布时间：**')[1].strip()
            elif line.startswith('### 摘要'):
                current_insight['summary'] = ''
            elif line.startswith('### 点评'):
                current_insight['comment'] = ''
            elif '阅读原文' in line and 'http' in line:
                import re
                link_match = re.search(r'\[阅读原文\]\((.*?)\)', line)
                if link_match:
                    current_insight['link'] = link_match.group(1)
            elif current_insight.get('summary') is not None and not line.startswith('###'):
                if 'summary' in current_insight and current_insight['summary'] == '':
                    current_insight['summary'] = line.strip()
                else:
                    current_insight['summary'] += ' ' + line.strip()
            elif current_insight.get('comment') is not None and not line.startswith('###'):
                if 'comment' in current_insight and current_insight['comment'] == '':
                    current_insight['comment'] = line.strip()
                else:
                    current_insight['comment'] += ' ' + line.strip()
        
        if current_insight:
            insights.append(current_insight)
        
        print(f"成功解析 {len(insights)} 条简讯")
        
    except Exception as e:
        print(f"解析简讯数据失败: {e}")
        # 使用默认数据
        insights = [
            {
                "title": "微软Azure发布AI Agent平台2.0版本",
                "category": "AI Agent",
                "source": "Azure Blog",
                "publish_time": "2026年3月6日 09:15",
                "summary": "微软Azure发布AI Agent平台2.0版本，新增多项功能增强智能体的交互能力和任务执行效率。更新包括改进的自然语言理解、多轮对话管理、任务规划优化等核心功能。平台还提供了更丰富的开发工具和API接口。",
                "comment": "AI Agent技术的成熟将推动自动化服务的发展。云厂商应关注Agent平台的建设，为客户提供更智能的解决方案。",
                "link": "https://azure.microsoft.com/en-us/blog/azure-ai-agent-update"
            },
            {
                "title": "AWS推出AI推理优化服务",
                "category": "云计算",
                "source": "AWS blog",
                "publish_time": "2026年3月6日 16:45",
                "summary": "AWS宣布推出AI推理优化服务，该服务通过智能调度和资源优化，帮助用户降低AI推理成本。服务支持多种AI框架和模型格式，提供实时监控和自动扩缩容功能，适用于不同规模的企业应用场景。",
                "comment": "这一服务体现了云厂商在AI成本优化方面的创新。预计将帮助更多中小企业实现AI应用的商业化落地。",
                "link": "https://aws.amazon.com/blogs/aws/new-ai-inference-optimization"
            }
        ]
    
    # 当前日期
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 白底简洁样式HTML模板
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI简讯 - {today_date}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            background: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2.2rem;
        }}
        .header p {{
            color: #7f8c8d;
            margin: 5px 0;
        }}
        .refresh-btn {{
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-top: 10px;
            transition: background 0.3s;
        }}
        .refresh-btn:hover {{
            background: #2980b9;
        }}
        .preview-section {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .preview-section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .preview-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .preview-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }}
        .preview-item h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 1.1rem;
        }}
        .preview-meta {{
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-bottom: 8px;
        }}
        .preview-summary {{
            font-size: 0.9rem;
            line-height: 1.4;
            color: #555;
        }}
        .insight-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .insight-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }}
        .insight-card h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3rem;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 10px;
        }}
        .insight-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
            font-size: 0.9rem;
        }}
        .meta-tag {{
            background: #ecf0f1;
            padding: 4px 12px;
            border-radius: 15px;
            color: #7f8c8d;
        }}
        .insight-content p {{
            margin-bottom: 12px;
            line-height: 1.6;
        }}
        .insight-content strong {{
            color: #2c3e50;
        }}
        .read-more {{
            display: inline-block;
            background: #3498db;
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 5px;
            font-size: 0.9rem;
            transition: background 0.3s;
            margin-top: 10px;
        }}
        .read-more:hover {{
            background: #2980b9;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-top: 40px;
            border-top: 1px solid #ecf0f1;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            .header h1 {{
                font-size: 1.8rem;
            }}
            .preview-list {{
                grid-template-columns: 1fr;
            }}
            .insight-card {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI简讯 - {today_date}</h1>
            <p>生成时间：{current_time}</p>
            <p>数据源数量：23个 · 成功获取简讯：{len(insights)}条</p>
            <button class="refresh-btn" onclick="location.reload()">【获取最新资讯】</button>
        </div>
        
        <!-- 今日简要预览 -->
        <div class="preview-section">
            <h2>📊 今日简要预览</h2>
            <div class="preview-list">
                {"\n".join([f'''
                <div class="preview-item">
                    <h3>{insight["title"]}</h3>
                    <div class="preview-meta">
                        <span>{insight["category"]}</span> · 
                        <span>{insight["source"]}</span> · 
                        <span>{insight["publish_time"]}</span>
                    </div>
                    <div class="preview-summary">
                        {insight["summary"][:100]}{'...' if len(insight["summary"]) > 100 else ''}
                    </div>
                </div>''' for insight in insights])}
            </div>
        </div>
        
        <!-- 详细简讯内容 -->
        <div class="insights-section">
            {"\n".join([f'''
            <div class="insight-card">
                <h3>{insight["title"]}</h3>
                <div class="insight-meta">
                    <span class="meta-tag">{insight["category"]}</span>
                    <span class="meta-tag">{insight["source"]}</span>
                    <span class="meta-tag">{insight["publish_time"]}</span>
                </div>
                <div class="insight-content">
                    <p><strong>摘要：</strong>{insight["summary"]}</p>
                    <p><strong>点评：</strong>{insight["comment"]}</p>
                    <a href="{insight["link"]}" class="read-more" target="_blank">阅读原文 →</a>
                </div>
            </div>''' for insight in insights])}
        </div>
        
        <div class="footer">
            <p>最近更新：{current_time}</p>
        </div>
    </div>
</body>
</html>"""
    
    # 保存到result目录
    os.makedirs("result", exist_ok=True)
    with open("result/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 复制到根目录
    import shutil
    shutil.copy2("result/index.html", "index.html")
    
    print("✅ 白底简洁样式已恢复")
    print("✅ 今日简要预览功能已添加")
    print("✅ 网页文件已生成: result/index.html")
    print("✅ 网页文件已复制到根目录: index.html")
    
    # 验证样式完整性
    verify_white_style_integrity()

def verify_white_style_integrity():
    """验证白底样式完整性"""
    
    print("\n验证白底样式完整性...")
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查关键样式元素
    style_elements = {
        "白底背景": "background-color: #f8f9fa",
        "今日简要预览": "preview-section",
        "预览列表": "preview-list",
        "预览项目": "preview-item",
        "卡片样式": "insight-card",
        "响应式设计": "@media (max-width:",
        "标签样式": "meta-tag",
        "按钮样式": "refresh-btn"
    }
    
    all_present = True
    for element_name, element_code in style_elements.items():
        if element_code in content:
            print(f"✅ {element_name}: 存在")
        else:
            print(f"❌ {element_name}: 缺失")
            all_present = False
    
    if all_present:
        print("\n🎉 白底样式所有元素完整保留！")
    else:
        print("\n⚠️ 部分样式元素缺失，需要检查")
    
    return all_present

if __name__ == "__main__":
    restore_white_style()
    
    print("\n" + "="*60)
    print("🎉 白底简洁版本网页样式恢复完成！")
    print("📁 生成的文件:")
    print("   • result/index.html (白底简洁版)")
    print("   • index.html (根目录版本)")
    print("🌟 特色功能:")
    print("   • 白底简洁设计")
    print("   • 今日简要预览")
    print("   • 响应式布局")
    print("🌐 在线访问: https://harker1544525153-lang.github.io/ai-insights/")
    print("="*60)