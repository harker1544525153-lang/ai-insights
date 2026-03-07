# AI简讯数据采集模块

import requests
import feedparser
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import re
from pathlib import Path
import logging
from typing import List, Dict, Optional

class AICrawler:
    """AI简讯数据采集器"""
    
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def fetch_rss_feed(self, url: str, source_name: str) -> List[Dict]:
        """获取RSS源数据"""
        try:
            self.logger.info(f"正在获取RSS源: {source_name}")
            
            if self.test_mode:
                # 测试模式下返回模拟数据
                return self._generate_test_data(source_name)
            
            # 解析RSS
            feed = feedparser.parse(url)
            
            if not feed.entries:
                self.logger.warning(f"RSS源 {source_name} 没有找到文章")
                return []
            
            articles = []
            for entry in feed.entries[:10]:  # 限制每个源最多10篇文章
                # 检查文章日期（只保留最近2天的文章）
                published = self._parse_date(entry)
                if not self._is_recent(published):
                    continue
                
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': self._clean_summary(entry.summary if hasattr(entry, 'summary') else ''),
                    'published': published,
                    'source': source_name,
                    'content': entry.get('content', [{}])[0].get('value', '') if hasattr(entry, 'content') else ''
                }
                articles.append(article)
            
            self.logger.info(f"从 {source_name} 获取到 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            self.logger.error(f"获取RSS源 {source_name} 失败: {e}")
            return []
    
    def fetch_web_content(self, url: str, source_name: str) -> List[Dict]:
        """获取网页内容"""
        try:
            self.logger.info(f"正在获取网页: {source_name}")
            
            if self.test_mode:
                # 测试模式下返回模拟数据
                return self._generate_test_data(source_name)
            
            # 这里可以扩展为使用Selenium等工具获取动态内容
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 简单的HTML解析（实际应用中可以使用BeautifulSoup等库）
            articles = self._parse_html_content(response.text, source_name)
            
            self.logger.info(f"从 {source_name} 获取到 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            self.logger.error(f"获取网页 {source_name} 失败: {e}")
            return []
    
    def fetch_all_sources(self, max_sources: int = 10) -> List[Dict]:
        """获取所有数据源的内容"""
        self.logger.info("开始采集所有数据源...")
        
        # 加载数据源配置
        from source.AI_sources import AIDataSourceManager
        data_manager = AIDataSourceManager()
        sources = data_manager.load_sources()
        
        if sources.empty:
            self.logger.error("没有找到可用的数据源")
            return []
        
        all_articles = []
        processed_count = 0
        
        for _, source in sources.iterrows():
            if processed_count >= max_sources:
                break
                
            source_name = source['name']
            source_type = source['type']
            source_url = source['url']
            
            if source_type == 'rss':
                articles = self.fetch_rss_feed(source_url, source_name)
            else:
                articles = self.fetch_web_content(source_url, source_name)
            
            all_articles.extend(articles)
            processed_count += 1
            
            # 避免请求过于频繁
            time.sleep(1)
        
        self.logger.info(f"总共获取到 {len(all_articles)} 篇文章")
        return all_articles
    
    def save_raw_data(self, articles: List[Dict]):
        """保存原始数据"""
        try:
            raw_dir = Path("data")
            raw_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            filename = f"raw_articles_{timestamp}.json"
            filepath = raw_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'generated_time': datetime.now().isoformat(),
                    'total_articles': len(articles),
                    'articles': articles
                }, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"原始数据已保存到: {filepath}")
            
        except Exception as e:
            self.logger.error(f"保存原始数据失败: {e}")
    
    def cleanup(self):
        """清理资源"""
        self.session.close()
    
    def _parse_date(self, entry) -> Optional[datetime]:
        """解析日期"""
        date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
        
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                return datetime.fromtimestamp(time.mktime(getattr(entry, field)))
        
        return datetime.now()
    
    def _is_recent(self, date: Optional[datetime]) -> bool:
        """检查是否为最近的文章（2天内）"""
        if not date:
            return False
        
        cutoff_date = datetime.now() - timedelta(days=2)
        return date >= cutoff_date
    
    def _clean_summary(self, summary: str) -> str:
        """清理摘要文本"""
        if not summary:
            return ""
        
        # 移除HTML标签
        summary = re.sub(r'<[^>]+>', '', summary)
        # 移除多余空格
        summary = re.sub(r'\s+', ' ', summary).strip()
        # 限制长度
        if len(summary) > 300:
            summary = summary[:297] + "..."
        
        return summary
    
    def _parse_html_content(self, html: str, source_name: str) -> List[Dict]:
        """解析HTML内容（简化版）"""
        # 这里可以实现具体的HTML解析逻辑
        # 目前返回模拟数据
        return self._generate_test_data(source_name)
    
    def _generate_test_data(self, source_name: str) -> List[Dict]:
        """生成测试数据"""
        test_articles = {
            'AWS blog': [
                {
                    'title': 'Amazon Bedrock推出新功能，支持更复杂的AI推理任务',
                    'link': 'https://aws.amazon.com/blogs/aws/new-amazon-bedrock-features/',
                    'summary': 'AWS宣布Amazon Bedrock新增多项功能，包括增强的推理能力和更灵活的模型配置选项。',
                    'published': datetime.now() - timedelta(hours=2),
                    'source': 'AWS blog'
                }
            ],
            '阿里云（微信公众号）': [
                {
                    'title': '阿里云发布通义千问2.5版本，性能大幅提升',
                    'link': 'https://example.com/aliyun-article',
                    'summary': '阿里云正式发布通义千问2.5版本，在多项基准测试中表现优异，推理速度提升30%。',
                    'published': datetime.now() - timedelta(hours=5),
                    'source': '阿里云（微信公众号）'
                }
            ],
            'NVIDIA blog': [
                {
                    'title': 'NVIDIA推出新一代AI芯片，专为大模型优化',
                    'link': 'https://blogs.nvidia.com/blog/new-ai-chip/',
                    'summary': 'NVIDIA发布专为大语言模型训练优化的新一代AI芯片，算力密度提升50%。',
                    'published': datetime.now() - timedelta(hours=1),
                    'source': 'NVIDIA blog'
                }
            ]
        }
        
        return test_articles.get(source_name, [])

# 简化的数据处理器
class AIProcessor:
    """AI简讯数据处理器"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """处理文章数据"""
        self.logger.info("开始处理文章数据...")
        
        # 去重
        unique_articles = self._remove_duplicates(articles)
        
        # 分类
        categorized_articles = self._categorize_articles(unique_articles)
        
        # 计算优先级
        prioritized_articles = self._calculate_priority(categorized_articles)
        
        # 排序
        sorted_articles = sorted(prioritized_articles, key=lambda x: x['priority'], reverse=True)
        
        # 限制数量
        final_articles = sorted_articles[:10]
        
        self.logger.info(f"处理完成，最终保留 {len(final_articles)} 篇文章")
        return final_articles
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """去除重复文章"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            title = article['title'].lower().strip()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        return unique_articles
    
    def _categorize_articles(self, articles: List[Dict]) -> List[Dict]:
        """分类文章"""
        # 加载分类配置
        categories_config = self._load_categories()
        
        for article in articles:
            article['category'] = self._assign_category(article, categories_config)
        
        return articles
    
    def _calculate_priority(self, articles: List[Dict]) -> List[Dict]:
        """计算优先级"""
        for article in articles:
            # 基于分类、来源、时效性等因素计算优先级
            priority = 5.0  # 基础优先级
            
            # 分类权重
            category_weights = {
                '大模型': 1.2, 'AI Agent': 1.1, '算力': 1.3,
                '政策合规': 0.8, '行业方案': 0.9, '云计算': 1.0,
                '开源': 0.7, '商业化': 0.8, '安全': 0.9,
                '企业服务': 0.8, '技术趋势': 1.1
            }
            
            if article['category'] in category_weights:
                priority *= category_weights[article['category']]
            
            # 来源权重
            source_weights = {
                'AWS blog': 1.2, 'Azure Blog': 1.2, 'NVIDIA blog': 1.3,
                '阿里云（微信公众号）': 1.1, '腾讯研究院（微信公众号）': 1.0
            }
            
            if article['source'] in source_weights:
                priority *= source_weights[article['source']]
            
            article['priority'] = round(min(priority, 10.0), 1)  # 限制在10分以内
        
        return articles
    
    def _load_categories(self) -> List[Dict]:
        """加载分类配置"""
        try:
            with open('categories.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('categories', [])
        except:
            # 默认分类配置
            return [
                {"name": "大模型", "keywords": ["gpt", "大模型", "llm", "语言模型"]},
                {"name": "AI Agent", "keywords": ["agent", "智能体", "自主ai"]},
                {"name": "算力", "keywords": ["gpu", "tpu", "ai芯片", "计算卡"]}
            ]
    
    def _assign_category(self, article: Dict, categories: List[Dict]) -> str:
        """分配分类"""
        title = article['title'].lower()
        summary = article.get('summary', '').lower()
        
        text = title + " " + summary
        
        for category in categories:
            keywords = category.get('keywords', [])
            for keyword in keywords:
                if keyword.lower() in text:
                    return category['name']
        
        return '技术趋势'  # 默认分类

# 简化的AI内容生成器
class AIGenerator:
    """AI内容生成器"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_insights(self, articles: List[Dict]) -> List[Dict]:
        """生成AI洞察"""
        self.logger.info("开始生成AI洞察...")
        
        insights = []
        for i, article in enumerate(articles):
            insight = self._generate_insight(article, i + 1)
            insights.append(insight)
        
        self.logger.info(f"生成 {len(insights)} 条AI洞察")
        return insights
    
    def _generate_insight(self, article: Dict, index: int) -> Dict:
        """生成单条洞察"""
        # 这里可以集成真实的AI模型来生成内容
        # 目前使用模板化的内容生成
        
        insight = {
            'id': index,
            'title': article['title'],
            'link': article['link'],
            'source': article['source'],
            'category': article.get('category', '技术趋势'),
            'priority': article.get('priority', 5.0),
            'summary': self._generate_summary(article),
            'comment': self._generate_comment(article),
            'cloud_perspective': self._generate_cloud_perspective(article),
            'generated_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return insight
    
    def _generate_summary(self, article: Dict) -> str:
        """生成摘要"""
        if article.get('summary'):
            return article['summary']
        
        # 基于标题生成简单摘要
        title = article['title']
        if '发布' in title or '推出' in title:
            return f"{title}，该技术/产品在相关领域具有重要影响。"
        elif '合作' in title or '达成' in title:
            return f"{title}，此次合作将推动相关技术的发展和应用。"
        else:
            return f"{title}，这是AI领域的重要进展，值得关注。"
    
    def _generate_comment(self, article: Dict) -> str:
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
    
    def _generate_cloud_perspective(self, article: Dict) -> Dict:
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
    # 测试数据采集功能
    crawler = AICrawler(test_mode=True)
    articles = crawler.fetch_all_sources(max_sources=3)
    
    print(f"获取到 {len(articles)} 篇文章")
    for article in articles:
        print(f"- {article['title']} ({article['source']})")
    
    # 测试数据处理功能
    processor = AIProcessor()
    processed_articles = processor.process_articles(articles)
    
    print(f"\n处理后保留 {len(processed_articles)} 篇文章")
    
    # 测试内容生成功能
    generator = AIGenerator()
    insights = generator.generate_insights(processed_articles)
    
    print(f"\n生成 {len(insights)} 条AI洞察")