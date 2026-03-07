# AI简讯生成系统v3.0 - 增强版主程序

import sys
from pathlib import Path
from datetime import datetime
import json
import pandas as pd

# 添加模块路径
sys.path.append(str(Path(__file__).parent))

from source.AI_sources_updated import AIDataSourceManager, initialize_sources_config
from crawler_enhanced import EnhancedAICrawler, process_articles, generate_insights

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime("%Y-%m-%d")

class AIInsightGenerator:
    """AI简讯生成器主类"""
    
    def __init__(self, test_mode=False, max_sources=10):
        self.test_mode = test_mode
        self.max_sources = max_sources
        self.data_source_manager = AIDataSourceManager()
        self.crawler = EnhancedAICrawler(test_mode=test_mode)
        
        self.start_time = None
        self.end_time = None
        self.sources_stats = []
    
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
            articles = self.crawler.fetch_all_sources(sources)
            
            if not articles:
                print("❌ 未采集到任何文章")
                return False
            
            print(f"✅ 成功采集 {len(articles)} 篇文章")
            
            # 4. 保存原始数据
            print("💾 保存原始数据...")
            self.crawler.save_raw_data(articles)
            
            # 5. 处理数据（去重、分类、排序）
            print("🔧 处理数据...")
            processed_articles = process_articles(articles)
            
            if not processed_articles:
                print("❌ 数据处理后无有效文章")
                return False
            
            print(f"✅ 处理后保留 {len(processed_articles)} 篇文章")
            
            # 6. AI生成摘要和点评
            print("🧠 AI生成内容...")
            insights = generate_insights(processed_articles)
            
            if not insights:
                print("❌ 未生成有效的AI洞察")
                return False
            
            print(f"✅ 生成 {len(insights)} 条AI洞察")
            
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
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清理资源
            self.crawler.cleanup()
    
    def generate_source_statistics(self, sources, articles):
        """生成数据源统计信息"""
        print("📈 生成数据源统计...")
        
        # 按数据源统计文章数量
        source_counts = {}
        for article in articles:
            source = article['source']
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # 生成统计信息
        self.sources_stats = []
        for _, source in sources.iterrows():
            source_name = source['name']
            count = source_counts.get(source_name, 0)
            
            stat = {
                'name': source_name,
                'type': self.data_source_manager.get_source_type(source),
                'category': source['category'],
                'priority': source['priority'],
                'article_count': count,
                'status': '成功' if count > 0 else '无数据'
            }
            self.sources_stats.append(stat)
        
        # 保存统计信息
        self.save_source_statistics()
    
    def save_source_statistics(self):
        """保存数据源统计信息"""
        source_dir = Path("source")
        source_dir.mkdir(exist_ok=True)
        
        # 保存为JSON
        stats_file = source_dir / "resultAI.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_time': datetime.now().isoformat(),
                'total_sources': len(self.sources_stats),
                'sources': self.sources_stats
            }, f, ensure_ascii=False, indent=2)
        
        # 保存为Excel
        df = pd.DataFrame(self.sources_stats)
        excel_file = source_dir / "resultAI.xlsx"
        df.to_excel(excel_file, index=False)
        
        print(f"✅ 数据源统计已保存到: {excel_file}")
    
    def generate_outputs(self, insights):
        """生成输出文件"""
        result_dir = Path("result")
        result_dir.mkdir(exist_ok=True)
        
        # 生成Markdown文件
        self.generate_markdown(insights, result_dir)
        
        # 生成JSON文件
        self.generate_json(insights, result_dir)
        
        # 生成HTML文件
        self.generate_html(insights, result_dir)
        
        # 生成历史存档
        self.generate_history(insights, result_dir)
    
    def generate_markdown(self, insights, result_dir):
        """生成Markdown文件"""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        
        # 生成详细Markdown
        md_content = f"""# AI行业每日洞察 · {get_current_date()}

## 📊 系统运行统计
- **开始时间**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
- **结束时间**: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}
- **运行时长**: {(self.end_time - self.start_time).total_seconds() / 60:.1f} 分钟
- **处理数据源**: {len(self.sources_stats)} 个
- **获取文章数**: {sum(stat['article_count'] for stat in self.sources_stats)} 篇
- **最终简讯**: {len(insights)} 条

## 📋 今日AI简讯

"""
        
        for insight in insights:
            md_content += f"""### {insight['id']}. {insight['title']}

**分类**: {insight['category']} | **优先级**: {insight['priority']}

**摘要**: {insight['summary']}

**点评**: {insight['comment']}

**来源**: {insight['source']} | **发布时间**: {insight['published']}

[阅读原文]({insight['link']})

---

"""
        
        # 保存详细Markdown
        detailed_file = result_dir / f"每日AI洞察简讯_{timestamp}.md"
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 保存简化版Markdown（用于分享）
        simple_content = f"""# AI简讯【{get_current_date()}】

"""
        
        for insight in insights:
            simple_content += f"""{insight['id']}、【{insight['title']}】
摘要：{insight['summary']}
点评：{insight['comment']}
原文链接：{insight['link']}

"""
        
        simple_content += f"""
详见原文网址：https://harker1544525153-lang.github.io/ai-insights/
"""
        
        latest_file = result_dir / "latest.md"
        with open(latest_file, 'w', encoding='utf-8') as f:
            f.write(simple_content)
        
        print(f"✅ Markdown文件已生成: {latest_file}")
    
    def generate_json(self, insights, result_dir):
        """生成JSON文件"""
        json_data = {
            'generated_time': datetime.now().isoformat(),
            'date': get_current_date(),
            'total_insights': len(insights),
            'insights': insights,
            'statistics': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat(),
                'duration_minutes': (self.end_time - self.start_time).total_seconds() / 60,
                'total_sources': len(self.sources_stats),
                'sources_stats': self.sources_stats
            }
        }
        
        # 保存最新JSON
        latest_json = result_dir / "latest.json"
        with open(latest_json, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON文件已生成: {latest_json}")
    
    def generate_html(self, insights, result_dir):
        """生成HTML文件"""
        # 读取优化后的HTML模板
        html_template_path = result_dir / "index_optimized.html"
        
        if html_template_path.exists():
            with open(html_template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 保存为index.html
            index_file = result_dir / "index.html"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML文件已生成: {index_file}")
        else:
            print("⚠️ HTML模板文件不存在，跳过HTML生成")
    
    def generate_history(self, insights, result_dir):
        """生成历史存档"""
        history_dir = result_dir / "history"
        history_dir.mkdir(exist_ok=True)
        
        # 保存历史JSON
        history_json = history_dir / f"{get_current_date()}.json"
        json_data = {
            'date': get_current_date(),
            'insights': insights,
            'generated_time': datetime.now().isoformat()
        }
        
        with open(history_json, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 历史存档已保存: {history_json}")
    
    def print_summary(self):
        """打印运行摘要"""
        if not self.start_time or not self.end_time:
            return
        
        duration = (self.end_time - self.start_time).total_seconds() / 60
        
        print(f"\n📊 运行摘要:")
        print(f"   开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   结束时间: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   运行时长: {duration:.1f} 分钟")
        print(f"   处理数据源: {len(self.sources_stats)} 个")
        print(f"   获取文章数: {sum(stat['article_count'] for stat in self.sources_stats)} 篇")
        print(f"   最终简讯: {len([s for s in self.sources_stats if s['article_count'] > 0])} 条")
        
        # 显示数据源统计
        print(f"\n📈 数据源统计:")
        for stat in self.sources_stats:
            status_icon = "✅" if stat['article_count'] > 0 else "❌"
            print(f"   {status_icon} {stat['name']}: {stat['article_count']} 篇文章")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI简讯生成系统v3.0')
    parser.add_argument('--test', action='store_true', help='测试模式')
    parser.add_argument('--max-sources', type=int, default=10, help='最大数据源数量')
    
    args = parser.parse_args()
    
    # 创建生成器实例
    generator = AIInsightGenerator(test_mode=args.test, max_sources=args.max_sources)
    
    # 执行生成
    success = generator.run_daily_generation()
    
    if success:
        generator.print_summary()
        print(f"\n🎯 所有文件已生成到 result/ 目录")
        print(f"📱 访问 index.html 查看网页版简讯")
        print(f"📄 查看 latest.md 获取文本版简讯")
    else:
        print("\n❌ AI简讯生成失败")
    
    return 0 if success else 1

if __name__ == "__main__":
    # 测试系统
    print("🧪 测试AI简讯生成系统...")
    
    generator = AIInsightGenerator(test_mode=True)
    success = generator.run_daily_generation()
    
    if success:
        generator.print_summary()
        print("\n🎉 系统测试完成！")
    else:
        print("\n❌ 系统测试失败")
    
    sys.exit(0 if success else 1)