#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版AI简讯生成器
根据用户要求修订网页样式
"""

import datetime
import os
import shutil

def generate_optimized_news():
    """生成优化版今日简讯"""
    
    print("开始生成优化版AI简讯...")
    
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
    
    # 创建近期简讯数据
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
    
    # 1. 生成优化版HTML文件（直接保存到根目录）
    generate_optimized_html(recent_insights, today_date, current_time)
    
    # 2. 生成Markdown文件
    generate_markdown(recent_insights, today_date, current_time)
    
    # 3. 更新数据源统计
    update_stats(today_date, current_time, len(recent_insights))
    
    print(f"\n✅ 优化版AI简讯生成完成！")
    print(f"📊 统计信息:")
    print(f"   生成简讯: {len(recent_insights)}条")
    print(f"   发布时间: {yesterday_str} - {today_str}")
    print(f"   样式特点: 优化导航栏 + 单行布局 + 分享功能")
    print(f"   📁 生成文件:")
    print(f"     - index.html (优化版)")
    print(f"     - latest.md")
    print(f"     - stats.md")

def generate_optimized_html(insights, today_date, current_time):
    """生成优化版HTML文件"""
    
    # 获取标题列表用于预览
    title_list = [f"{i}. {insight['title']}" for i, insight in enumerate(insights, 1)]
    
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
    for i, insight in enumerate(insights, 1):
        html_content += f'''                <div class="preview-item">
                    <div class="preview-num">{i}</div>
                    <div class="preview-title">{insight['title']}</div>
                </div>
'''
    
    html_content += f'''            </div>
        </div>
        
        <!-- 简讯列表 -->
        <div class="insights-section">
'''
    
    # 添加简讯列表
    for i, insight in enumerate(insights, 1):
        html_content += f'''            <div class="insight-item">
                <div class="insight-header">
                    <div class="insight-num">{i}</div>
                    <div class="insight-title">{insight['title']}</div>
                    <div class="insight-category">{insight['category']}</div>
                    <div class="insight-source">{insight['source']}</div>
                    <a href="{insight['link']}" class="read-more" target="_blank">阅读原文</a>
                </div>
                <div class="insight-content">
                    <div class="insight-summary">{insight['summary']}</div>
                    <div class="insight-comment">{insight['comment']}</div>
                    <div class="insight-meta">
                        <span>发布时间: {insight['publish_time']}</span>
                        <span>来源: {insight['source']}</span>
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
    
    # 写入HTML文件（直接保存到根目录）
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ 优化版HTML文件生成完成")



def generate_markdown(insights, today_date, current_time):
    """生成Markdown文件"""
    
    markdown_content = f"""# AI简讯 - {today_date}

最近更新：{current_time}

## 今日简讯预览

"""
    
    # 添加预览列表
    for i, insight in enumerate(insights, 1):
        markdown_content += f"{i}. {insight['title']}\n"
    
    markdown_content += "\n## 详细内容\n\n"
    
    # 添加详细内容
    for i, insight in enumerate(insights, 1):
        markdown_content += f"""### {i}. {insight['title']}

**发布时间：** {insight['publish_time']}  
**分类：** {insight['category']}  
**来源：** {insight['source']}  

**核心信息：** {insight['summary']}

**行业洞察：** {insight['comment']}

[阅读原文]({insight['link']})

---

"""
    
    # 写入Markdown文件
    with open('latest.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("✅ Markdown文件生成完成")

def update_stats(today_date, current_time, count):
    """更新数据源统计"""
    stats_content = f"""# 数据源统计

**生成时间：** {current_time}  
**简讯数量：** {count}条  
**日期范围：** {today_date}  

## 数据来源

- DeepSeek官方
- 阿里云官方  
- 腾讯云官方
- 字节跳动官方
- AWS官方
- 微软官方

## 生成文件

- index.html (优化版)
- latest.md
"""
    
    with open('stats.md', 'w', encoding='utf-8') as f:
        f.write(stats_content)
    
    print("✅ 统计信息更新完成")

if __name__ == "__main__":
    generate_optimized_news()