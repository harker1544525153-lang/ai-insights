# AI简讯生成系统v3.0 - 增强版数据采集器

import requests
import feedparser
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json
import time
import logging
from typing import List, Dict, Any
import re

class EnhancedAICrawler:
    """增强版AI简讯数据采集器"""
    
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        self.setup_logging()
    
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/crawler.log'),
                logging.StreamHandler()
            ]
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
            for entry in feed.entries[:15]:  # 限制每个源最多15篇文章
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
            self.logger.info(f"正在获取网页内容: {source_name}")
            
            if self.test_mode:
                # 测试模式下返回模拟数据
                return self._generate_test_data(source_name)
            
            # 获取网页内容
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 尝试提取文章列表（根据常见网站结构）
            articles = self._extract_articles_from_html(soup, source_name, url)
            
            if not articles:
                self.logger.warning(f"网页 {source_name} 没有找到文章")
                return []
            
            self.logger.info(f"从 {source_name} 获取到 {len(articles)} 篇文章")
            return articles
            
        except Exception as e:
            self.logger.error(f"获取网页内容 {source_name} 失败: {e}")
            return []
    
    def _extract_articles_from_html(self, soup: BeautifulSoup, source_name: str, base_url: str) -> List[Dict]:
        """从HTML中提取文章"""
        articles = []
        
        # 常见的选择器模式
        selectors = [
            'article',
            '.article',
            '.post',
            '.news-item',
            '.blog-post',
            'h2 a',
            'h3 a',
            '.title a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:10]:  # 限制数量
                    try:
                        title = self._extract_title(element)
                        link = self._extract_link(element, base_url)
                        
                        if title and link:
                            article = {
                                'title': title,
                                'link': link,
                                'summary': '',
                                'published': datetime.now(),
                                'source': source_name,
                                'content': ''
                            }
                            articles.append(article)
                    except Exception as e:
                        self.logger.debug(f"提取文章信息失败: {e}")
                
                if articles:
                    break
        
        return articles
    
    def _extract_title(self, element) -> str:
        """提取标题"""
        if hasattr(element, 'get_text'):
            return element.get_text().strip()
        elif hasattr(element, 'text'):
            return element.text.strip()
        return ""
    
    def _extract_link(self, element, base_url: str) -> str:
        """提取链接"""
        if hasattr(element, 'get'):
            href = element.get('href', '')
            if href:
                if href.startswith('http'):
                    return href
                else:
                    return base_url.rstrip('/') + '/' + href.lstrip('/')
        return ""
    
    def _parse_date(self, entry) -> datetime:
        """解析日期"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                return datetime(*entry.updated_parsed[:6])
            else:
                return datetime.now()
        except:
            return datetime.now()
    
    def _is_recent(self, date: datetime) -> bool:
        """检查是否为近期文章（最近2天）"""
        return (datetime.now() - date).days <= 2
    
    def _clean_summary(self, summary: str) -> str:
        """清理摘要"""
        # 移除HTML标签
        summary = re.sub(r'<[^>]+>', '', summary)
        # 限制长度
        if len(summary) > 200:
            summary = summary[:197] + '...'
        return summary.strip()
    
    def _generate_test_data(self, source_name: str) -> List[Dict]:
        """生成测试数据"""
        test_articles = [
            {
                'title': f'{source_name}测试文章1 - AI技术新突破',
                'link': f'https://example.com/{source_name}/article1',
                'summary': f'这是来自{source_name}的测试文章摘要，展示了AI技术的最新发展。',
                'published': datetime.now() - timedelta(hours=2),
                'source': source_name,
                'content': f'这是来自{source_name}的完整文章内容，包含详细的技术分析和市场洞察。'
            },
            {
                'title': f'{source_name}测试文章2 - 云计算趋势分析',
                'link': f'https://example.com/{source_name}/article2',
                'summary': f'这是来自{source_name}的另一篇测试文章，探讨云计算的最新趋势。',
                'published': datetime.now() - timedelta(hours=5),
                'source': source_name,
                'content': f'这是来自{source_name}的完整文章内容，详细分析云计算市场的发展方向。'
            }
        ]
        return test_articles
    
    def fetch_all_sources(self, sources_df: pd.DataFrame) -> List[Dict]:
        """获取所有数据源的文章"""
        all_articles = []
        
        for _, source in sources_df.iterrows():
            source_name = source['name']
            
            # 获取URL
            url = self._get_source_url(source)
            if not url:
                self.logger.warning(f"数据源 {source_name} 缺少有效的URL")
                continue
            
            # 根据类型获取数据
            if self._get_source_type(source) == 'rss':
                articles = self.fetch_rss_feed(url, source_name)
            else:
                articles = self.fetch_web_content(url, source_name)
            
            all_articles.extend(articles)
            
            # 避免请求过于频繁
            time.sleep(1)
        
        return all_articles
    
    def _get_source_url(self, source_row) -> str:
        """获取数据源的URL"""
        if 'rss_url' in source_row and pd.notna(source_row['rss_url']) and source_row['rss_url']:
            return source_row['rss_url']
        elif 'home_url' in source_row and pd.notna(source_row['home_url']) and source_row['home_url']:
            return source_row['home_url']
        else:
            return ""
    
    def _get_source_type(self, source_row) -> str:
        """获取数据源类型"""
        if 'rss_url' in source_row and pd.notna(source_row['rss_url']) and source_row['rss_url']:
            return 'rss'
        else:
            return 'web'
    
    def save_raw_data(self, articles: List[Dict]):
        """保存原始数据"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # 转换日期为字符串格式
        serializable_articles = []
        for article in articles:
            serializable_article = article.copy()
            serializable_article['published'] = article['published'].isoformat()
            serializable_articles.append(serializable_article)
        
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"raw_articles_{timestamp}.json"
        filepath = data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_time': datetime.now().isoformat(),
                'total_articles': len(articles),
                'articles': serializable_articles
            }, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"原始数据已保存到: {filepath}")
    
    def cleanup(self):
        """清理资源"""
        self.session.close()

def process_articles(articles: List[Dict]) -> List[Dict]:
    """处理文章数据"""
    if not articles:
        return []
    
    # 去重（基于标题和链接）
    seen = set()
    unique_articles = []
    
    for article in articles:
        key = f"{article['title']}|{article['link']}"
        if key not in seen:
            seen.add(key)
            unique_articles.append(article)
    
    # 按发布时间排序（最新的在前）
    unique_articles.sort(key=lambda x: x['published'], reverse=True)
    
    # 限制数量（最多20篇）
    return unique_articles[:20]

def generate_insights(articles: List[Dict]) -> List[Dict]:
    """生成AI洞察"""
    insights = []
    
    for i, article in enumerate(articles[:10]):  # 最多10条洞察
        insight = {
            'id': i + 1,
            'title': article['title'],
            'category': '技术趋势',  # 简化分类
            'priority': 5,  # 默认优先级
            'summary': article['summary'] or article['title'],
            'comment': f'来自{article["source"]}的最新AI资讯',
            'source': article['source'],
            'link': article['link'],
            'published': article['published'].strftime('%Y-%m-%d %H:%M') if isinstance(article['published'], datetime) else article['published']
        }
        insights.append(insight)
    
    return insights

if __name__ == "__main__":
    # 测试增强版采集器
    crawler = EnhancedAICrawler(test_mode=True)
    
    # 创建测试数据源
    test_sources = pd.DataFrame([
        {
            'name': 'AWS blog',
            'type': 'rss',
            'rss_url': 'https://aws.amazon.com/blogs/aws/feed/',
            'home_url': 'https://aws.amazon.com/blogs/aws/',
            'category': '云计算',
            'priority': 10,
            'enabled': 1
        },
        {
            'name': '36氪（AI频道）',
            'type': 'web',
            'rss_url': '',
            'home_url': 'https://36kr.com/',
            'category': '技术趋势',
            'priority': 7,
            'enabled': 1
        }
    ])
    
    print("🧪 测试增强版数据采集器...")
    
    # 获取数据
    articles = crawler.fetch_all_sources(test_sources)
    print(f"✅ 成功采集 {len(articles)} 篇文章")
    
    # 处理数据
    processed_articles = process_articles(articles)
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
        print(f"   链接: {insight['link']}")
    
    # 保存数据
    crawler.save_raw_data(articles)
    
    print("\n🎉 增强版数据采集器测试完成！")