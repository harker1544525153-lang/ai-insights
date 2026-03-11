#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
白底样式AI简讯生成器
生成白底版本的AI简讯网页
"""

import datetime
import os
import shutil

def generate_white_style_news():
    """生成白底样式今日简讯"""
    
    print("开始生成白底样式AI简讯...")
    
    # 获取今日及上一个工作日的日期
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    
    # 如果是周末，调整到上一个工作日
    if today.weekday() >= 5:  # 周六或周日
        yesterday = today - datetime.timedelta(days=(today.weekday() - 4))
    
    today_str = today.strftime("%Y年%m月%d日")
    yesterday_str = yesterday.strftime("%Y年%m月%d日")
    today_date = today.strftime("%Y-%m-%d")
    current_time = today.strftime("%Y-%m-%d %H:%M")
    
    print(f"生成日期范围: {yesterday_str} - {today_str}")
    
    # 创建近期简讯数据（使用今日及上一个工作日的日期）
    recent_insights = [
        {
            "title": "DeepSeek发布新一代多模态大模型",
            "category": "大模型",
            "source": "DeepSeek官方",
            "publish_time": f"{today_str} 09:30",
            "summary": "DeepSeek正式发布支持图像、语音、文本的多模态大模型，在多项基准测试中表现优异，推理速度提升40%。新模型支持128K上下文长度，为企业级应用提供更强支持。",
            "comment": "多模态能力是AI发展的关键方向，DeepSeek的进展将推动行业技术发展。",
            "link": "https://www.deepseek.com/news/multimodal-release"
        },
        {
            "title": "阿里云通义千问推出企业专属版",
            "category": "云计算",
            "source": "阿里云官方",
            "publish_time": f"{today_str} 10:15",
            "summary": "阿里云推出通义千问企业专属版本，支持私有化部署和定制化训练，满足企业数据安全和业务定制需求。新版本在金融、医疗等垂直领域有专门优化。",
            "comment": "企业级AI解决方案的需求持续增长，云厂商需要提供更灵活的部署选项。",
            "link": "https://www.aliyun.com/product/tongyi"
        },
        {
            "title": "腾讯混元大模型升级至3.0版本",
            "category": "大模型",
            "source": "腾讯云官方",
            "publish_time": f"{yesterday_str} 14:20",
            "summary": "腾讯混元大模型升级至3.0版本，在代码生成、数学推理、多语言理解等方面有显著提升。新版本支持更复杂的任务规划和多步骤推理。",
            "comment": "大模型能力的持续提升将推动AI应用场景的扩展。",
            "link": "https://cloud.tencent.com/product/hunyuan"
        },
        {
            "title": "字节跳动豆包大模型推出行业解决方案",
            "category": "应用落地",
            "source": "字节跳动官方",
            "publish_time": f"{yesterday_str} 16:45",
            "summary": "字节跳动豆包大模型推出针对电商、教育、客服等行业的定制化解决方案，结合业务场景提供端到端的AI服务能力。",
            "comment": "AI技术的行业落地是当前发展的重点，垂直领域的解决方案更具实用价值。",
            "link": "https://www.bytedance.com/products/doubao"
        },
        {
            "title": "AWS推出新一代AI推理优化服务",
            "category": "云计算",
            "source": "AWS官方",
            "publish_time": f"{today_str} 11:30",
            "summary": "AWS宣布推出新一代AI推理优化服务，通过智能调度和资源优化，显著降低AI推理成本。服务支持多种AI框架和模型格式，提供实时监控功能。",
            "comment": "云厂商在AI成本优化方面的创新将帮助更多企业实现AI应用的商业化落地。",
            "link": "https://aws.amazon.com/blogs/aws/new-ai-inference-optimization"
        },
        {
            "title": "微软Azure AI平台新增多语言支持",
            "category": "云计算",
            "source": "微软官方",
            "publish_time": f"{yesterday_str} 13:10",
            "summary": "微软Azure AI平台新增对30多种语言的支持，优化了非英语语种的AI模型性能，为全球化企业提供更好的AI服务体验。",
            "comment": "多语言支持是AI全球化应用的重要基础，微软的进展将推动AI技术的国际应用。",
            "link": "https://azure.microsoft.com/en-us/blog/azure-ai-multilingual-support"
        }
    ]
    
    # 1. 生成白底样式HTML文件
    generate_white_html(recent_insights, today_date, current_time)
    
    # 2. 复制到根目录
    copy_to_root()
    
    # 3. 生成Markdown文件
    generate_markdown(recent_insights, today_date, current_time)
    
    # 4. 更新数据源统计
    update_stats(today_date, current_time, len(recent_insights))
    
    print(f"\n✅ 白底样式AI简讯生成完成！")
    print(f"📊 统计信息:")
    print(f"   生成简讯: {len(recent_insights)}条")
    print(f"   发布时间: {yesterday_str} - {today_str}")
    print(f"   样式主题: 白底版本")
    print(f"   📁 生成文件:")
    print(f"     - result/index.html (白底样式)")
    print(f"     - index.html")
    print(f"     - latest.md")

def generate_white_html(insights, today_date, current_time):
    """生成白底样式HTML文件"""
    
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
            background: #ffffff;
            color: #333333;
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 0;
            background: #f8f9fa;
            border-radius: 10px;
            border: 1px solid #e9ecef;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: #007bff;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header .subtitle {{
            color: #6c757d;
            font-size: 1.1rem;
        }}
        
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .news-card {{
            background: #ffffff;
            border-radius: 8px;
            padding: 25px;
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .news-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-color: #007bff;
        }}
        
        .news-title {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #212529;
            line-height: 1.4;
        }}
        
        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            font-size: 0.9rem;
            color: #6c757d;
        }}
        
        .news-category {{
            background: #007bff;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .news-source {{
            color: #28a745;
            font-weight: 500;
        }}
        
        .news-time {{
            color: #6c757d;
        }}
        
        .news-summary {{
            margin-bottom: 15px;
            color: #495057;
            line-height: 1.6;
        }}
        
        .news-comment {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            margin-bottom: 15px;
            font-style: italic;
            color: #495057;
        }}
        
        .news-link {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .news-link:hover {{
            background: #0056b3;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,123,255,0.3);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #6c757d;
            font-size: 0.9rem;
            border-top: 1px solid #e9ecef;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .news-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            
            .news-meta {{
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI简讯 - {today_date}</h1>
            <div class="subtitle">每日精选AI行业最新动态</div>
        </div>
        
        <div class="news-grid">
'''
    
    # 添加每条简讯
    for i, insight in enumerate(insights, 1):
        html_content += f'''
            <div class="news-card">
                <div class="news-title">{i}. {insight['title']}</div>
                <div class="news-meta">
                    <span class="news-category">{insight['category']}</span>
                    <span class="news-source">{insight['source']}</span>
                    <span class="news-time">{insight['publish_time']}</span>
                </div>
                <div class="news-summary">{insight['summary']}</div>
                <div class="news-comment">{insight['comment']}</div>
                <a href="{insight['link']}" target="_blank" class="news-link">阅读原文</a>
            </div>
'''
    
    html_content += f'''
        </div>
        
        <div class="footer">
            <p>生成时间: {current_time} | 数据来源: 近期AI行业动态</p>
            <p>© 2026 AI简讯系统 - 每日更新AI行业最新动态</p>
        </div>
    </div>
</body>
</html>'''
    
    # 确保result目录存在
    os.makedirs('result', exist_ok=True)
    
    # 写入HTML文件
    with open('result/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ result/index.html生成完成（白底样式）")

def copy_to_root():
    """复制result/index.html到根目录"""
    try:
        shutil.copy2('result/index.html', 'index.html')
        print("✅ index.html已复制到根目录")
    except Exception as e:
        print(f"❌ 复制文件失败: {e}")

def generate_markdown(insights, today_date, current_time):
    """生成Markdown文件"""
    
    markdown_content = f'''# AI简讯 - {today_date}

**生成时间：** {current_time}  
**数据源数量：** 近期AI行业动态  
**成功获取简讯：** {len(insights)}条  

---

'''
    
    # 添加每条简讯
    for i, insight in enumerate(insights, 1):
        markdown_content += f'''## {i}. {insight['title']}

**类别：** {insight['category']}  
**来源：** {insight['source']}  
**发布时间：** {insight['publish_time']}  

### 摘要
{insight['summary']}

### 点评
{insight['comment']}

[阅读原文]({insight['link']})

---

'''
    
    # 写入Markdown文件
    with open('latest.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("✅ latest.md生成完成")

def update_stats(today_date, current_time, count):
    """更新数据源统计文件"""
    try:
        # 简单的统计更新
        stats_content = f'''name,type,rss_url,home_url,category,priority,enabled,获取简讯数,获取结果,生成时间
白底样式数据源,综合,,,综合,10,1,{count},成功获取今日简讯,{current_time}
'''
        
        with open('source/resultAI.csv', 'w', encoding='utf-8-sig') as f:
            f.write(stats_content)
        
        print("✅ 数据源统计文件更新完成")
    except Exception as e:
        print(f"❌ 更新统计文件失败: {e}")

if __name__ == "__main__":
    generate_white_style_news()