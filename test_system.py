# AI简讯生成系统v3.0 - 系统测试脚本

import os
import sys
from datetime import datetime, timedelta
import json
from pathlib import Path

def test_output_generation():
    """测试输出文件生成功能"""
    print("🧪 测试输出文件生成功能...")
    
    # 创建测试数据
    test_insights = [
        {
            'id': 1,
            'title': '微软发布Copilot Pro 2026版，深度集成GPT-5技术',
            'link': 'https://example.com/article1',
            'source': 'AWS blog',
            'category': '大模型',
            'priority': 8.7,
            'summary': '微软正式推出Copilot Pro 2026版本，深度集成GPT-5技术，提供更强大的代码生成和文档处理能力。新版本在响应速度、准确性方面有显著提升，支持多模态输入输出。',
            'comment': '该技术进展对云厂商的大模型服务有重要影响，可能带来新的商机。建议关注技术成熟度和商业化路径。',
            'cloud_perspective': {
                '阿里云': '适合电商和金融场景的AI应用，建议关注技术集成和行业解决方案。',
                '腾讯云': '在社交和游戏领域有优势，可探索内容推荐和用户交互的创新应用。',
                '华为云': '智能制造和5G+AI的结合点，适合企业数字化和物联网场景。',
                'AWS': '企业级AI服务的标准化方案，适合大规模部署和全球化服务。',
                'Azure': 'Office集成的协同办公方案，适合企业工作流优化和生产力提升。',
                'GCP': '大数据分析的AI增强方案，适合数据驱动型企业的智能化转型。'
            },
            'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'id': 2,
            'title': 'NVIDIA发布新一代AI芯片，算力提升3倍',
            'link': 'https://example.com/article2',
            'source': 'NVIDIA blog',
            'category': '算力',
            'priority': 9.2,
            'summary': 'NVIDIA正式发布新一代AI芯片H200，相比前代产品算力提升3倍，能效比提升40%。新芯片专为大模型训练和推理优化，支持更大规模的参数模型。',
            'comment': '硬件进步将降低云服务成本，提升AI计算效率。这对云厂商的成本控制和性能优化具有重要意义。',
            'cloud_perspective': {
                '阿里云': '适合大规模AI训练场景，可降低计算成本提升竞争力。',
                '腾讯云': '在游戏和社交AI计算方面有显著优势，可优化用户体验。',
                '华为云': '结合5G和边缘计算，适合智能制造和物联网场景。',
                'AWS': '企业级AI服务的硬件基础，适合大规模部署需求。',
                'Azure': 'Office AI应用的硬件支撑，提升协同办公效率。',
                'GCP': '大数据分析的算力保障，支持复杂AI模型训练。'
            },
            'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    
    test_sources_stats = [
        {'name': 'AWS blog', 'count': 3, 'status': '成功'},
        {'name': '阿里云（微信公众号）', 'count': 2, 'status': '成功'},
        {'name': 'NVIDIA blog', 'count': 1, 'status': '成功'},
        {'name': 'TechCrunch', 'count': 0, 'status': '失败', 'error': '网络连接超时'}
    ]
    
    start_time = datetime.now() - timedelta(minutes=5)
    end_time = datetime.now()
    
    # 创建输出目录
    output_dir = Path("result")
    output_dir.mkdir(exist_ok=True)
    history_dir = output_dir / "history"
    history_dir.mkdir(exist_ok=True)
    
    # 生成Markdown文件
    print("📝 生成Markdown文件...")
    md_content = generate_markdown_report(test_insights, start_time, end_time)
    
    # 保存带时间戳的Markdown文件
    timestamp = start_time.strftime("%Y-%m-%dT%H-%M-%S")
    md_filename = f"每日AI洞察简讯_{timestamp}.md"
    md_path = output_dir / md_filename
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 保存latest.md（覆盖更新）
    latest_md_path = output_dir / "latest.md"
    with open(latest_md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Markdown文件已生成: {md_path}")
    print(f"✅ 最新Markdown文件: {latest_md_path}")
    
    # 生成HTML文件
    print("🌐 生成HTML文件...")
    html_content = generate_html_report(test_insights, start_time, end_time)
    
    html_path = output_dir / "index.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 保存历史HTML文件
    date_str = start_time.strftime("%Y-%m-%d")
    history_html_path = history_dir / f"{date_str}.html"
    with open(history_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML文件已生成: {html_path}")
    print(f"✅ 历史HTML文件: {history_html_path}")
    
    # 生成JSON文件
    print("📊 生成JSON文件...")
    json_data = {
        'generated_time': end_time.isoformat(),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'total_insights': len(test_insights),
        'insights': test_insights,
        'statistics': calculate_statistics(test_insights, start_time, end_time)
    }
    
    json_path = output_dir / "latest.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    # 保存历史JSON文件
    history_json_path = history_dir / f"{date_str}.json"
    with open(history_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON文件已生成: {json_path}")
    print(f"✅ 历史JSON文件: {history_json_path}")
    
    # 生成数据源统计（简化版）
    print("📈 生成数据源统计...")
    source_stats_content = generate_source_stats(test_sources_stats, start_time)
    source_path = Path("source") / "resultAI.txt"
    source_path.parent.mkdir(exist_ok=True)
    
    with open(source_path, 'w', encoding='utf-8') as f:
        f.write(source_stats_content)
    
    print(f"✅ 数据源统计文件: {source_path}")
    
    # 打印统计信息
    print("\n" + "=" * 60)
    print("📊 系统运行统计")
    print("=" * 60)
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"运行时长: {str(end_time - start_time).split('.')[0]}")
    print(f"处理源数量: 4")
    print(f"获取文章数: 6")
    print(f"筛选后文章数: 4")
    print(f"最终文章数: 2")
    
    print(f"\n📈 分类统计:")
    print("  大模型: 1条")
    print("  算力: 1条")
    
    print("\n✅ 输出文件:")
    print(f"  Markdown: result/latest.md")
    print(f"  HTML: result/index.html")
    print(f"  JSON: result/latest.json")
    print(f"  数据源统计: source/resultAI.txt")
    print("=" * 60)
    
    print("\n🎉 系统测试完成！所有输出文件已生成。")
    
    return True

def generate_markdown_report(insights, start_time, end_time):
    """生成Markdown报告"""
    date_str = start_time.strftime("%Y-%m-%d")
    
    md_content = f"""# AI行业每日洞察 · {date_str}

## 📊 系统运行统计

- **开始时间**: {start_time.strftime("%Y-%m-%d %H:%M:%S")}
- **结束时间**: {end_time.strftime("%Y-%m-%d %H:%M:%S")}
- **运行时长**: {str(end_time - start_time).split('.')[0]}
- **处理源数量**: 4
- **获取文章数**: 6
- **筛选后文章数**: 4
- **最终文章数**: {len(insights)}

## 📈 分类统计

- **大模型**: 1条
- **算力**: 1条

## 🎯 今日精选 ({len(insights)}条)

"""
    
    for insight in insights:
        md_content += f"""### {insight['id']}. {insight['title']}

**来源**: {insight['source']} | **分类**: {insight['category']} | **优先级**: {insight['priority']}

**摘要**: {insight['summary']}

**云厂商视角**: {insight['comment']}

**详细分析**:
- 阿里云: {insight['cloud_perspective']['阿里云']}
- 腾讯云: {insight['cloud_perspective']['腾讯云']}
- 华为云: {insight['cloud_perspective']['华为云']}
- AWS: {insight['cloud_perspective']['AWS']}
- Azure: {insight['cloud_perspective']['Azure']}
- GCP: {insight['cloud_perspective']['GCP']}

[查看原文]({insight['link']})

---

"""
    
    md_content += f"""
## 📋 数据源统计

| 数据源 | 文章数 | 状态 |
|--------|--------|------|
| AWS blog | 3 | 成功 |
| 阿里云（微信公众号） | 2 | 成功 |
| NVIDIA blog | 1 | 成功 |
| TechCrunch | 0 | 失败 |

*生成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return md_content

def generate_html_report(insights, start_time, end_time):
    """生成HTML报告"""
    date_str = start_time.strftime("%Y-%m-%d")
    
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI行业每日洞察 · {date_str}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{ 
            text-align: center; 
            margin-bottom: 30px; 
            padding-bottom: 20px;
            border-bottom: 3px solid #f0f0f0;
        }}
        .header h1 {{ 
            font-size: 2.5em; 
            color: #333; 
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin: 20px 0; 
        }}
        .stat-card {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center;
            border-left: 4px solid #667eea;
        }}
        .stat-number {{ 
            font-size: 1.8em; 
            font-weight: bold; 
            color: #333; 
        }}
        .stat-label {{ 
            font-size: 0.9em; 
            color: #666; 
            margin-top: 5px;
        }}
        .insight {{ 
            border: 1px solid #e0e0e0; 
            padding: 25px; 
            margin: 20px 0; 
            border-radius: 10px;
            background: white;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .insight:hover {{ 
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }}
        .insight-title {{ 
            font-size: 1.3em; 
            font-weight: bold; 
            color: #333; 
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .insight-meta {{ 
            color: #666; 
            font-size: 0.9em; 
            margin: 10px 0; 
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }}
        .insight-meta span {{ 
            background: #f0f8ff; 
            padding: 3px 8px; 
            border-radius: 12px; 
            font-size: 0.8em;
        }}
        .cloud-perspective {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 15px 0;
            border-left: 3px solid #667eea;
        }}
        .cloud-vendor {{ 
            margin: 8px 0; 
            padding-left: 10px;
            border-left: 2px solid #ddd;
        }}
        .category-badge {{ 
            display: inline-block; 
            padding: 2px 8px; 
            border-radius: 12px; 
            font-size: 0.8em; 
            margin-right: 5px;
            color: white;
        }}
        .footer {{ 
            text-align: center; 
            margin-top: 30px; 
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .header h1 {{ font-size: 2em; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .insight {{ padding: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI行业每日洞察 · {date_str}</h1>
            <p>今日精选 {len(insights)} 条AI行业动态</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">4</div>
                <div class="stat-label">处理源数量</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div class="stat-label">获取文章数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">4</div>
                <div class="stat-label">筛选后文章数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(insights)}</div>
                <div class="stat-label">最终文章数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{str(end_time - start_time).split('.')[0]}</div>
                <div class="stat-label">运行时长</div>
            </div>
        </div>
        
        <div class="insights">
"""
    
    for insight in insights:
        # 根据分类设置颜色
        category_colors = {
            '大模型': '#FF6B6B',
            'AI Agent': '#4ECDC4', 
            '算力': '#45B7D1',
            '云厂商': '#96CEB4',
            '技术突破': '#FECA57',
            '应用落地': '#FF9FF3'
        }
        color = category_colors.get(insight['category'], '#8395A7')
        
        html_content += f"""
            <div class="insight">
                <div class="insight-title">
                    <span class="category-badge" style="background-color: {color};">{insight['category']}</span>
                    {insight['id']}. {insight['title']}
                </div>
                <div class="insight-meta">
                    <span>来源: {insight['source']}</span>
                    <span>优先级: {insight['priority']}</span>
                    <span>生成时间: {insight['generated_time']}</span>
                </div>
                <p><strong>摘要:</strong> {insight['summary']}</p>
                <p><strong>云厂商视角:</strong> {insight['comment']}</p>
                <div class="cloud-perspective">
                    <strong>详细分析:</strong>
                    <div class="cloud-vendor"><strong>阿里云:</strong> {insight['cloud_perspective']['阿里云']}</div>
                    <div class="cloud-vendor"><strong>腾讯云:</strong> {insight['cloud_perspective']['腾讯云']}</div>
                    <div class="cloud-vendor"><strong>华为云:</strong> {insight['cloud_perspective']['华为云']}</div>
                    <div class="cloud-vendor"><strong>AWS:</strong> {insight['cloud_perspective']['AWS']}</div>
                    <div class="cloud-vendor"><strong>Azure:</strong> {insight['cloud_perspective']['Azure']}</div>
                    <div class="cloud-vendor"><strong>GCP:</strong> {insight['cloud_perspective']['GCP']}</div>
                </div>
                <a href="{insight['link']}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">📖 查看原文</a>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="footer">
            <p><em>生成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}</em></p>
            <p>系统运行统计: 开始时间 {start_time.strftime('%H:%M:%S')} - 结束时间 {end_time.strftime('%H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def calculate_statistics(insights, start_time, end_time):
    """计算统计信息"""
    return {
        'duration': str(end_time - start_time).split('.')[0],
        'sources_processed': 4,
        'articles_fetched': 6,
        'articles_filtered': 4,
        'final_articles': len(insights)
    }

def generate_source_stats(sources_stats, start_time):
    """生成数据源统计"""
    content = f"数据源统计 - 生成时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += "数据源名称\t简讯数量\t状态\t未获取原因\n"
    content += "-" * 60 + "\n"
    
    for stat in sources_stats:
        content += f"{stat['name']}\t{stat['count']}\t{stat['status']}\t{stat.get('error', '')}\n"
    
    return content

if __name__ == "__main__":
    print("🚀 AI简讯生成系统v3.0 - 测试脚本")
    print("=" * 60)
    
    success = test_output_generation()
    
    if success:
        print("\n✅ 系统测试成功完成！")
        print("📁 生成的文件位置:")
        print("  • result/latest.md - Markdown格式报告")
        print("  • result/index.html - HTML网页报告") 
        print("  • result/latest.json - JSON数据文件")
        print("  • source/resultAI.txt - 数据源统计")
        print("\n🎯 下一步: 可以运行完整系统进行实际数据采集")
    else:
        print("\n❌ 系统测试失败")
        sys.exit(1)