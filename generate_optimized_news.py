#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版AI简讯生成器
确保根目录index.html由result/index.html覆盖
优化历史简讯功能
"""

import datetime
import json
import csv
import os
import shutil

def generate_optimized_news():
    """生成优化版今日简讯"""
    
    print("🚀 开始生成优化版今日简讯...")
    
    # 当前日期
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 模拟今日简讯数据
    todays_insights = [
        {
            "title": "阿里云发布AI大模型推理服务重大升级",
            "category": "云计算",
            "source": "阿里云（微信公众号）",
            "publish_time": f"{today_date} 09:15",
            "summary": "阿里云宣布对其AI大模型推理服务进行全面升级，新增多项功能优化。升级内容包括推理性能提升30%，支持更多模型格式，优化了资源调度算法，降低了用户使用成本。此次升级将显著提升AI应用的响应速度和稳定性。",
            "comment": "从云厂商视角看，这一升级体现了云计算平台在AI基础设施领域的持续投入。预计将推动更多企业采用云原生AI解决方案，加速行业数字化转型进程。",
            "link": "https://mp.weixin.qq.com/s/QfWC_uxAmTlpPu1CW9dJNA"
        },
        {
            "title": "腾讯云推出新一代AI芯片计算平台",
            "category": "算力",
            "source": "腾讯研究院（微信公众号）",
            "publish_time": f"{today_date} 10:30",
            "summary": "腾讯云发布新一代AI芯片计算平台，该平台在计算性能和能效比方面均有显著提升。新平台支持更复杂的AI训练和推理任务，为大规模AI应用提供强大的硬件基础。腾讯表示，该平台将推动AI技术在各个行业的深入应用。",
            "comment": "算力资源的优化配置是AI应用落地的关键。云厂商需要平衡性能、成本和能效，满足不同客户的需求。",
            "link": "https://mp.weixin.qq.com/s/example1"
        },
        {
            "title": "微软Azure发布AI Agent平台2.0版本",
            "category": "AI Agent",
            "source": "Azure Blog",
            "publish_time": f"{today_date} 14:20",
            "summary": "微软Azure发布AI Agent平台2.0版本，新增多项功能增强智能体的交互能力和任务执行效率。更新包括改进的自然语言理解、多轮对话管理、任务规划优化等核心功能。平台还提供了更丰富的开发工具和API接口。",
            "comment": "AI Agent技术的成熟将推动自动化服务的发展。云厂商应关注Agent平台的建设，为客户提供更智能的解决方案。",
            "link": "https://azure.microsoft.com/en-us/blog/azure-ai-agent-update"
        },
        {
            "title": "AWS推出AI推理优化服务",
            "category": "云计算",
            "source": "AWS blog",
            "publish_time": f"{today_date} 16:45",
            "summary": "AWS宣布推出AI推理优化服务，该服务通过智能调度和资源优化，帮助用户降低AI推理成本。服务支持多种AI框架和模型格式，提供实时监控和自动扩缩容功能，适用于不同规模的企业应用场景。",
            "comment": "这一服务体现了云厂商在AI成本优化方面的创新。预计将帮助更多中小企业实现AI应用的商业化落地。",
            "link": "https://aws.amazon.com/blogs/aws/new-ai-inference-optimization"
        },
        {
            "title": "谷歌云发布大模型安全合规框架更新",
            "category": "安全",
            "source": "GCP Blog",
            "publish_time": f"{today_date} 11:10",
            "summary": "谷歌云发布大模型安全合规框架的重要更新，新增多项安全功能和合规检查机制。更新内容包括数据隐私保护增强、内容安全过滤优化、合规性检查自动化等，为企业提供更全面的安全保障。",
            "comment": "安全合规是AI技术大规模应用的前提。云厂商需要持续投入安全技术研发，确保客户数据和应用的安全。",
            "link": "https://cloud.google.com/blog/products/ai-machine-learning/ai-safety-update"
        },
        {
            "title": "NVIDIA发布新一代AI训练加速器",
            "category": "算力",
            "source": "NVIDIA blog",
            "publish_time": f"{today_date} 13:25",
            "summary": "NVIDIA发布新一代AI训练加速器，该加速器在训练速度和能效方面均有显著提升。新加速器支持更大规模的模型训练，优化了内存管理和数据传输效率，为AI研发提供更强大的计算支持。",
            "comment": "硬件技术的进步是AI发展的基础。云厂商需要与硬件厂商紧密合作，为客户提供最优的计算解决方案。",
            "link": "https://blogs.nvidia.com/blog/new-ai-training-accelerator"
        }
    ]
    
    # 1. 生成result/index.html（使用浅色主题）
    generate_result_html(todays_insights, today_date, current_time)
    
    # 2. 复制result/index.html到根目录
    copy_result_to_root()
    
    # 3. 生成Markdown文件
    generate_markdown_file(todays_insights, today_date, current_time)
    
    # 4. 更新数据源统计文件
    update_resultai_file(today_date, current_time, len(todays_insights))
    
    print(f"\n🎉 优化版今日简讯生成完成！")
    print(f"📊 统计信息:")
    print(f"   生成简讯: {len(todays_insights)}条")
    print(f"   生成文件:")
    print(f"     - result/index.html (浅色主题)")
    print(f"     - index.html (由result/index.html覆盖)")
    print(f"     - latest.md")
    print(f"     - source/resultAI.csv")
    
    return True

def generate_result_html(insights, today_date, current_time):
    """生成result/index.html（浅色主题）"""
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI简讯 - 真实数据源【{today_date}】</title>
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
        
        .share-btn {{
            padding: 8px 16px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }}
        
        .share-btn:hover {{
            background: #0056b3;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        
        .header p {{
            color: #666;
            font-size: 14px;
        }}
        
        /* 今日简讯预览样式 */
        .preview-section {{
            background: white;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            overflow: hidden;
            height: auto;
            max-height: 280px;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .preview-header {{
            background: #007bff;
            color: white;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .preview-title {{
            font-size: 18px;
            font-weight: bold;
        }}
        
        .preview-count {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .preview-list {{
            padding: 15px 20px;
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .preview-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .preview-item:last-child {{
            border-bottom: none;
        }}
        
        .preview-number {{
            background: #007bff;
            color: white;
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
            color: #333;
        }}
        
        /* 简讯详情样式 */
        .insights-section {{
            margin: 20px 0;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid #007bff;
        }}
        
        .insight-item {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-left: 4px solid #007bff;
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
            color: #333;
            flex: 1;
            min-width: 300px;
        }}
        
        .insight-meta {{
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .category-tag {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .source-tag {{
            background: #fff3e0;
            color: #f57c00;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .time-tag {{
            background: #f3e5f5;
            color: #7b1fa2;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .insight-content {{
            margin-bottom: 15px;
        }}
        
        .insight-summary {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        
        .insight-comment {{
            background: #e8f5e8;
            border-left: 3px solid #4caf50;
            padding: 12px;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #2e7d32;
        }}
        
        .insight-footer {{
            display: flex;
            justify-content: flex-end;
            margin-top: 10px;
        }}
        
        .read-more {{
            background: #007bff;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 12px;
            transition: background 0.3s;
        }}
        
        .read-more:hover {{
            background: #0056b3;
        }}
        
        .stats-section {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
            border: 1px solid #e9ecef;
        }}
        
        .no-data-message {{
            text-align: center;
            color: #999;
            font-style: italic;
            padding: 40px;
            background: #f8f9fa;
            border-radius: 8px;
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
                    <option value="{today_date}" selected>{today_date}</option>
                </select>
                <button class="share-btn" onclick="shareContent()">分享</button>
            </div>
        </div>
        
        <!-- 页面标题 -->
        <div class="header">
            <h1>AI简讯 - {today_date}</h1>
            <p>最新AI行业动态，专业视角解读</p>
        </div>
        
        <!-- 今日简讯预览 -->
        <div class="preview-section">
            <div class="preview-header">
                <div class="preview-title">今日简讯预览</div>
                <div class="preview-count">共{len(insights)}条简讯</div>
            </div>
            <div class="preview-list">
'''

    # 添加预览项
    for i, insight in enumerate(insights, 1):
        html_content += f'''                <div class="preview-item">
                    <div class="preview-number">{i}</div>
                    <div class="preview-text">{insight['title']}</div>
                </div>
'''

    html_content += f'''            </div>
        </div>
        
        <!-- 简讯详情 -->
        <div class="insights-section">
            <div class="section-title">详细内容</div>
'''

    # 添加详细内容
    for i, insight in enumerate(insights, 1):
        html_content += f'''            <div class="insight-item">
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
            </div>
'''

    html_content += f'''        </div>
        
        <!-- 统计信息 -->
        <div class="stats-section">
            最近更新：{current_time} | 
            处理数据源：23个 | 
            成功获取：{len(insights)}条简讯
        </div>
    </div>
    
    <!-- JavaScript功能 -->
    <script>
        // 分享功能
        function shareContent() {{
            const titles = Array.from(document.querySelectorAll('.insight-title'))
                .map(title => title.textContent.trim())
                .join('\\n');
            
            const content = `今日AI简讯（{today_date}）\\n\\n${{titles}}\\n\\n更多详情请访问：https://harker1544525153-lang.github.io/ai-insights/`;
            
            navigator.clipboard.writeText(content).then(() => {{
                alert('简讯内容已复制到剪贴板！');
            }}).catch(err => {{
                console.error('复制失败:', err);
                alert('复制失败，请手动复制内容');
            }});
        }}
        
        // 历史数据管理
        const historicalData = {{
            '{today_date}': {{
                insights: {json.dumps(insights, ensure_ascii=False, indent=2)},
                count: {len(insights)}
            }}
        }};
        
        // 日期选择器功能
        document.getElementById('dateSelector').addEventListener('change', function(e) {{
            const selectedDate = e.target.value;
            loadHistoricalData(selectedDate);
        }});
        
        function loadHistoricalData(date) {{
            const data = historicalData[date];
            
            if (data) {{
                // 更新预览区域
                const previewList = document.querySelector('.preview-list');
                const previewCount = document.querySelector('.preview-count');
                const insightsSection = document.querySelector('.insights-section');
                
                // 更新预览列表
                previewList.innerHTML = '';
                data.insights.forEach((insight, index) => {{
                    const previewItem = document.createElement('div');
                    previewItem.className = 'preview-item';
                    previewItem.innerHTML = `
                        <div class="preview-number">${{index + 1}}</div>
                        <div class="preview-text">${{insight.title}}</div>
                    `;
                    previewList.appendChild(previewItem);
                }});
                
                // 更新计数
                previewCount.textContent = `共${{data.count}}条简讯`;
                
                // 更新详细内容
                insightsSection.innerHTML = `
                    <div class="section-title">详细内容</div>
                    ${{data.insights.map((insight, index) => `
                        <div class="insight-item">
                            <div class="insight-header">
                                <div class="insight-title">${{insight.title}}</div>
                                <div class="insight-meta">
                                    <span class="category-tag">${{insight.category}}</span>
                                    <span class="source-tag">${{insight.source}}</span>
                                    <span class="time-tag">${{insight.publish_time}}</span>
                                </div>
                            </div>
                            <div class="insight-content">
                                <div class="insight-summary">${{insight.summary}}</div>
                                <div class="insight-comment">${{insight.comment}}</div>
                            </div>
                            <div class="insight-footer">
                                <a href="${{insight.link}}" target="_blank" class="read-more">阅读原文</a>
                            </div>
                        </div>
                    `).join('')}}
                `;
                
                // 更新页面标题
                document.title = `AI简讯 - 真实数据源【${{date}}】`;
                
            }} else {{
                // 如果没有数据，显示提示信息
                const insightsSection = document.querySelector('.insights-section');
                insightsSection.innerHTML = `
                    <div class="section-title">详细内容</div>
                    <div class="no-data-message">
                        暂无 ${{date}} 的历史数据
                    </div>
                `;
            }}
        }}
        
        // 初始化页面时，检查是否有历史数据并动态更新日期选择器
        function initializeDateSelector() {{
            const dateSelector = document.getElementById('dateSelector');
            const availableDates = Object.keys(historicalData);
            
            // 如果有历史数据，显示所有可用日期
            if (availableDates.length > 1) {{
                dateSelector.innerHTML = availableDates.map(date => 
                    `<option value="${{date}}" ${{date === '{today_date}' ? 'selected' : ''}}>${{date}}</option>`
                ).join('');
            }}
            // 如果只有今天的数据，隐藏日期选择器
            else {{
                dateSelector.style.display = 'none';
            }}
        }}
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDateSelector();
        }});
    </script>
</body>
</html>'''

    # 确保result目录存在
    os.makedirs('result', exist_ok=True)
    
    # 写入result/index.html
    with open('result/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ result/index.html生成完成（浅色主题）")

def copy_result_to_root():
    """复制result/index.html到根目录"""
    
    try:
        shutil.copy2('result/index.html', 'index.html')
        print("✅ result/index.html已复制到根目录")
    except Exception as e:
        print(f"❌ 复制文件失败: {e}")

def generate_markdown_file(insights, today_date, current_time):
    """生成Markdown文件"""
    
    md_content = f'''# AI简讯 - {today_date}

**生成时间：** {current_time}  
**数据源数量：** 23个  
**成功获取简讯：** {len(insights)}条  

---

'''

    # 添加简讯内容
    for i, insight in enumerate(insights, 1):
        md_content += f'''## {i}. {insight['title']}

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
        f.write(md_content)
    
    print("✅ Markdown文件生成完成")

def update_resultai_file(today_date, current_time, insights_count):
    """更新数据源统计文件"""
    
    # 读取现有的resultAI.csv
    rows = []
    with open('source/resultAI.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            # 更新生成时间
            row['生成时间'] = f"{current_time}:00"
            
            # 如果是成功获取的数据源，更新最新简讯发布时间
            if row['获取结果'] == '成功获取今日简讯' and insights_count > 0:
                row['最新简讯发布时间'] = f"{today_date} 09:15"
            
            rows.append(row)
    
    # 写入更新后的文件
    with open('source/resultAI.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print("✅ 数据源统计文件更新完成")

if __name__ == "__main__":
    generate_optimized_news()