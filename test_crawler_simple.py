# 简化的数据采集测试脚本

import json
from datetime import datetime, timedelta
from pathlib import Path

def test_data_collection():
    """测试数据采集功能"""
    print("🧪 测试数据采集功能...")
    
    # 创建模拟数据
    test_articles = [
        {
            'title': 'AWS宣布Amazon Bedrock新增多项AI推理功能',
            'link': 'https://aws.amazon.com/blogs/aws/new-amazon-bedrock-features/',
            'summary': 'AWS宣布Amazon Bedrock新增多项功能，包括增强的推理能力和更灵活的模型配置选项。',
            'published': datetime.now() - timedelta(hours=2),
            'source': 'AWS blog'
        },
        {
            'title': '阿里云发布通义千问2.5版本，性能大幅提升',
            'link': 'https://example.com/aliyun-article',
            'summary': '阿里云正式发布通义千问2.5版本，在多项基准测试中表现优异，推理速度提升30%。',
            'published': datetime.now() - timedelta(hours=5),
            'source': '阿里云（微信公众号）'
        },
        {
            'title': 'NVIDIA推出新一代AI芯片，专为大模型优化',
            'link': 'https://blogs.nvidia.com/blog/new-ai-chip/',
            'summary': 'NVIDIA发布专为大语言模型训练优化的新一代AI芯片，算力密度提升50%。',
            'published': datetime.now() - timedelta(hours=1),
            'source': 'NVIDIA blog'
        },
        {
            'title': '微软Azure AI推出新的企业级解决方案',
            'link': 'https://azure.microsoft.com/blog/azure-ai-enterprise/',
            'summary': '微软Azure AI推出针对企业客户的新解决方案，集成GPT-4和Copilot技术。',
            'published': datetime.now() - timedelta(hours=3),
            'source': 'Azure Blog'
        }
    ]
    
    print(f"✅ 模拟采集到 {len(test_articles)} 篇文章")
    
    # 保存原始数据
    raw_dir = Path("data")
    raw_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"raw_articles_{timestamp}.json"
    filepath = raw_dir / filename
    
    # 转换日期为字符串格式
    serializable_articles = []
    for article in test_articles:
        serializable_article = article.copy()
        serializable_article['published'] = article['published'].isoformat()
        serializable_articles.append(serializable_article)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_time': datetime.now().isoformat(),
            'total_articles': len(test_articles),
            'articles': serializable_articles
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 原始数据已保存到: {filepath}")
    
    # 处理数据
    processed_articles = process_articles(test_articles)
    print(f"✅ 处理后保留 {len(processed_articles)} 篇文章")
    
    # 生成AI洞察
    insights = generate_insights(processed_articles)
    print(f"✅ 生成 {len(insights)} 条AI洞察")
    
    # 显示结果
    print("\n📊 生成的AI洞察:")
    for insight in insights:
        print(f"\n{insight['id']}. {insight['title']}")
        print(f"   分类: {insight['category']} | 优先级: {insight['priority']}")
        print(f"   来源: {insight['source']}")
        print(f"   摘要: {insight['summary']}")
    
    return insights

def process_articles(articles):
    """处理文章数据"""
    # 去重
    unique_articles = remove_duplicates(articles)
    
    # 分类
    categorized_articles = categorize_articles(unique_articles)
    
    # 计算优先级
    prioritized_articles = calculate_priority(categorized_articles)
    
    # 排序
    sorted_articles = sorted(prioritized_articles, key=lambda x: x['priority'], reverse=True)
    
    # 限制数量
    final_articles = sorted_articles[:10]
    
    return final_articles

def remove_duplicates(articles):
    """去除重复文章"""
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        title = article['title'].lower().strip()
        if title not in seen_titles:
            seen_titles.add(title)
            unique_articles.append(article)
    
    return unique_articles

def categorize_articles(articles):
    """分类文章"""
    categories = [
        {"name": "大模型", "keywords": ["gpt", "大模型", "llm", "语言模型", "千问", "文心一言", "通义"]},
        {"name": "AI Agent", "keywords": ["agent", "智能体", "自主ai", "agent平台", "自动化"]},
        {"name": "算力", "keywords": ["gpu", "tpu", "ai芯片", "计算卡", "数据中心", "算力"]},
        {"name": "云计算", "keywords": ["云服务", "云平台", "云原生", "云安全", "云计算"]},
        {"name": "技术趋势", "keywords": ["技术发展", "技术创新", "技术突破", "技术趋势"]}
    ]
    
    for article in articles:
        article['category'] = assign_category(article, categories)
    
    return articles

def assign_category(article, categories):
    """分配分类"""
    title = article['title'].lower()
    summary = article.get('summary', '').lower()
    
    text = title + " " + summary
    
    for category in categories:
        keywords = category.get('keywords', [])
        for keyword in keywords:
            if keyword.lower() in text:
                return category['name']
    
    return '技术趋势'

def calculate_priority(articles):
    """计算优先级"""
    for article in articles:
        priority = 5.0  # 基础优先级
        
        # 分类权重
        category_weights = {
            '大模型': 1.2, 'AI Agent': 1.1, '算力': 1.3,
            '云计算': 1.0, '技术趋势': 1.1
        }
        
        if article['category'] in category_weights:
            priority *= category_weights[article['category']]
        
        # 来源权重
        source_weights = {
            'AWS blog': 1.2, 'Azure Blog': 1.2, 'NVIDIA blog': 1.3,
            '阿里云（微信公众号）': 1.1
        }
        
        if article['source'] in source_weights:
            priority *= source_weights[article['source']]
        
        article['priority'] = round(min(priority, 10.0), 1)
    
    return articles

def generate_insights(articles):
    """生成AI洞察"""
    insights = []
    for i, article in enumerate(articles):
        insight = {
            'id': i + 1,
            'title': article['title'],
            'link': article['link'],
            'source': article['source'],
            'category': article.get('category', '技术趋势'),
            'priority': article.get('priority', 5.0),
            'summary': article.get('summary', ''),
            'comment': generate_comment(article),
            'cloud_perspective': generate_cloud_perspective(article),
            'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        insights.append(insight)
    
    return insights

def generate_comment(article):
    """生成云厂商视角点评"""
    category = article.get('category', '技术趋势')
    
    comments = {
        '大模型': '该技术进展对云厂商的大模型服务有重要影响，可能带来新的商机。',
        'AI Agent': '智能体技术的发展将推动云服务向更智能化的方向发展。',
        '算力': '硬件进步将降低云服务成本，提升AI计算效率。',
        '云计算': '云服务商需要关注技术集成和行业解决方案的创新。',
        '技术趋势': '这一趋势将影响云服务商的技术路线和产品策略。'
    }
    
    return comments.get(category, '该技术进展对云服务商具有重要战略意义。')

def generate_cloud_perspective(article):
    """生成云厂商详细分析"""
    return {
        '阿里云': '适合电商和金融场景的AI应用，建议关注技术集成和行业解决方案。',
        '腾讯云': '在社交和游戏领域有优势，可探索内容推荐和用户交互的创新应用。',
        '华为云': '智能制造和5G+AI的结合点，适合企业数字化和物联网场景。',
        'AWS': '企业级AI服务的标准化方案，适合大规模部署和全球化服务。',
        'Azure': 'Office集成的协同办公方案，适合企业工作流优化和生产力提升。',
        'GCP': '大数据分析的AI增强方案，适合数据驱动型企业的智能化转型。'
    }

if __name__ == "__main__":
    print("🚀 AI简讯数据采集测试")
    print("=" * 60)
    
    insights = test_data_collection()
    
    print(f"\n🎉 数据采集测试完成！")
    print(f"📊 生成 {len(insights)} 条AI洞察")
    print(f"📁 原始数据已保存到 data/ 目录")
    print(f"\n🎯 下一步: 可以运行完整系统进行实际数据采集")