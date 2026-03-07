# AI简讯生成系统v3.0 - 主程序

import argparse
import schedule
import time
from datetime import datetime
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import get_current_date, get_current_time, SCHEDULE_CONFIG
from crawler import AICrawler
from output import AIOutputGenerator
from source.AI_sources import AIDataSourceManager, initialize_sources_config

class AIInsightGenerator:
    """AI简讯生成器主类"""
    
    def __init__(self, test_mode=False, max_sources=10):
        self.test_mode = test_mode
        self.max_sources = max_sources
        self.data_source_manager = AIDataSourceManager()
        self.crawler = AICrawler()
        self.output_generator = AIOutputGenerator()
        
        self.start_time = None
        self.end_time = None
        self.sources_stats = []
        
        print("=" * 60)
        print("🤖 AI简讯生成系统v3.0")
        print("=" * 60)
        print(f"启动时间: {get_current_time()}")
        print(f"运行模式: {'测试模式' if test_mode else '生产模式'}")
        print(f"最大数据源: {max_sources}")
        print("=" * 60)
    
    def run_daily_generation(self):
        """执行每日简讯生成"""
        self.start_time = datetime.now()
        print(f"\n🚀 开始生成 {get_current_date()} 的AI简讯...")
        
        try:
            # 1. 初始化数据源
            print("📊 初始化数据源配置...")
            initialize_sources_config()
            
            # 2. 获取数据源
            print("🔍 加载数据源...")
            sources = self.data_source_manager.load_sources()
            
            if sources.empty:
                print("❌ 未找到可用的数据源")
                return False
            
            print(f"✅ 加载 {len(sources)} 个数据源")
            
            # 3. 采集数据
            print("🌐 开始采集AI资讯...")
            articles = self.crawler.fetch_all_sources()
            
            if not articles:
                print("❌ 未采集到任何文章")
                return False
            
            print(f"✅ 成功采集 {len(articles)} 篇文章")
            
            # 4. 保存原始数据
            print("💾 保存原始数据...")
            self.crawler.save_raw_data(articles)
            
            # 5. 处理数据（去重、分类、排序）
            print("🔧 处理数据...")
            processed_articles = self.process_articles(articles)
            
            # 6. AI生成摘要和点评
            print("🧠 AI生成内容...")
            insights = self.generate_insights(processed_articles)
            
            # 7. 生成数据源统计
            self.generate_source_statistics(sources, articles)
            
            # 8. 输出结果
            print("📤 生成输出文件...")
            self.end_time = datetime.now()
            self.generate_outputs(insights)
            
            print(f"\n🎉 {get_current_date()} AI简讯生成完成！")
            return True
            
        except Exception as e:
            print(f"❌ 生成过程中出现错误: {e}")
            return False
        finally:
            # 清理资源
            self.crawler.cleanup()
    
    def process_articles(self, articles):
        """处理文章数据"""
        processed = []
        
        # 去重（基于标题）
        seen_titles = set()
        for article in articles:
            title = article.get('title', '').strip().lower()
            if title and title not in seen_titles:
                seen_titles.add(title)
                
                # 添加处理后的字段
                article['processed_time'] = get_current_time()
                article['category'] = self.classify_article(article)
                article['priority_score'] = self.calculate_priority(article)
                
                processed.append(article)
        
        # 按优先级排序
        processed.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
        
        print(f"✅ 处理完成，去重后剩余 {len(processed)} 篇文章")
        return processed
    
    def classify_article(self, article):
        """文章分类"""
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()
        
        # 11个固定类别关键词匹配
        categories = {
            '大模型': ['gpt', '大模型', 'llm', '语言模型', '千问', '文心一言', '通义'],
            'AI Agent': ['agent', '智能体', '自主ai', 'agent平台', '自动化'],
            '算力': ['gpu', 'tpu', 'ai芯片', '计算卡', '数据中心', '算力'],
            '政策合规': ['政策', '法规', '标准', '监管', '安全', '合规'],
            '行业方案': ['行业应用', '解决方案', '落地案例', '实践'],
            '云计算': ['云服务', '云平台', '云原生', '云安全', '云计算'],
            '开源': ['开源项目', '开源工具', '开源框架', '开源'],
            '商业化': ['商业模式', '商业应用', '市场机会', '商业化'],
            '安全': ['网络安全', '数据安全', '应用安全', '安全'],
            '企业服务': ['企业应用', '企业软件', '企业平台', '企业服务'],
            '技术趋势': ['技术发展', '技术创新', '技术突破', '技术趋势']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title or keyword in content:
                    return category
        
        return '其他'
    
    def calculate_priority(self, article):
        """计算文章优先级"""
        score = 0
        
        # 源优先级
        source_priority = article.get('source_priority', 5)
        score += source_priority * 0.3
        
        # 标题长度（通常重要文章标题更详细）
        title_length = len(article.get('title', ''))
        score += min(title_length / 50, 1) * 0.2
        
        # 内容长度
        content_length = len(article.get('content', ''))
        score += min(content_length / 500, 1) * 0.3
        
        # 时效性（简化处理）
        score += 0.2
        
        return round(score, 2)
    
    def generate_insights(self, articles):
        """生成AI洞察"""
        insights = []
        
        for i, article in enumerate(articles[:10]):  # 只处理前10篇
            insight = {
                'id': i + 1,
                'title': article['title'],
                'link': article['link'],
                'source': article['source_name'],
                'category': article['category'],
                'priority': article['priority_score'],
                'summary': self.generate_summary(article),
                'comment': self.generate_comment(article),
                'cloud_perspective': self.generate_cloud_perspective(article),
                'generated_time': get_current_time()
            }
            insights.append(insight)
        
        return insights
    
    def generate_summary(self, article):
        """生成摘要（200-300字）"""
        title = article['title']
        content = article.get('content', '')
        
        # 简化实现，实际应该调用AI模型生成200-300字摘要
        if len(content) > 200:
            summary = content[:200] + '...'
        else:
            summary = content
        
        return f"{title}。{summary}"
    
    def generate_comment(self, article):
        """生成点评（2-3句深度分析）"""
        category = article['category']
        
        comments = {
            '大模型': '该技术进展对云厂商的大模型服务有重要影响，可能带来新的商机。建议关注技术成熟度和商业化路径。',
            'AI Agent': '智能体技术的发展将推动云厂商在自动化服务方面的创新。需要评估技术可行性和市场需求。',
            '算力': '硬件进步将降低云服务成本，提升AI计算效率。这对云厂商的成本控制和性能优化具有重要意义。',
            '云计算': '云服务创新将推动企业数字化转型。云厂商需要关注技术趋势和客户需求变化。',
            '行业方案': '实际应用案例为云厂商提供了可复制的解决方案。建议分析行业痛点和解决方案的有效性。'
        }
        
        return comments.get(category, '该动态值得云厂商关注，可能带来新的业务机会。建议深入分析技术价值和市场潜力。')
    
    def generate_cloud_perspective(self, article):
        """生成云厂商视角分析"""
        return {
            '阿里云': '适合电商和金融场景的AI应用，建议关注技术集成和行业解决方案。',
            '腾讯云': '在社交和游戏领域有优势，可探索内容推荐和用户交互的创新应用。',
            '华为云': '智能制造和5G+AI的结合点，适合企业数字化和物联网场景。',
            'AWS': '企业级AI服务的标准化方案，适合大规模部署和全球化服务。',
            'Azure': 'Office集成的协同办公方案，适合企业工作流优化和生产力提升。',
            'GCP': '大数据分析的AI增强方案，适合数据驱动型企业的智能化转型。'
        }
    
    def generate_source_statistics(self, sources, articles):
        """生成数据源统计"""
        self.sources_stats = []
        
        for _, source in sources.iterrows():
            source_name = source['name']
            
            # 统计该数据源的文章数量
            article_count = sum(1 for article in articles if article.get('source_name') == source_name)
            
            # 判断状态
            status = '成功' if article_count > 0 else '失败'
            error_msg = '' if article_count > 0 else '未获取到文章'
            
            self.sources_stats.append({
                'name': source_name,
                'count': article_count,
                'status': status,
                'error': error_msg
            })
    
    def generate_outputs(self, insights):
        """生成所有输出文件"""
        success = self.output_generator.generate_all_outputs(
            insights, 
            self.sources_stats, 
            self.start_time, 
            self.end_time
        )
        
        if success:
            print("✅ 输出文件生成完成")
        else:
            print("❌ 输出文件生成失败")
    
    def setup_scheduler(self):
        """设置定时任务"""
        print("⏰ 设置定时任务...")
        
        # 早上8点执行
        schedule.every().day.at(SCHEDULE_CONFIG['morning_run']).do(self.run_daily_generation)
        
        # 早上8:30备份执行
        schedule.every().day.at(SCHEDULE_CONFIG['morning_backup']).do(self.run_daily_generation)
        
        print(f"✅ 定时任务已设置: {SCHEDULE_CONFIG['morning_run']} 和 {SCHEDULE_CONFIG['morning_backup']}")
        
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI简讯生成系统v3.0')
    parser.add_argument('--test', action='store_true', help='测试模式')
    parser.add_argument('--max-sources', type=int, default=10, help='最大数据源数量')
    parser.add_argument('--schedule', action='store_true', help='启用定时任务')
    parser.add_argument('--auto', action='store_true', help='自动化模式（用于GitHub Actions）')
    
    args = parser.parse_args()
    
    # 创建生成器实例
    generator = AIInsightGenerator(test_mode=args.test, max_sources=args.max_sources)
    
    if args.schedule:
        # 定时任务模式
        generator.setup_scheduler()
    elif args.auto:
        # 自动化模式（GitHub Actions）
        print("🚀 启动自动化模式（GitHub Actions）")
        success = generator.run_daily_generation()
        if success:
            print("✅ 自动化任务执行成功")
        else:
            print("❌ 自动化任务执行失败")
        sys.exit(0 if success else 1)
    else:
        # 立即执行模式
        success = generator.run_daily_generation()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()