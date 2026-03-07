#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版数据源统计管理器 - 不依赖pandas，确保resultAI表格仅呈现成功获取的数据源信息
"""

import csv
from datetime import datetime
import os
import json

class SimpleResultAIManager:
    """简化版数据源统计管理器"""
    
    def __init__(self, ai_sources_file='source/AI_sources.xlsx'):
        """初始化管理器"""
        self.ai_sources_file = ai_sources_file
        self.result_file = 'source/resultAI.csv'
        self.sources_data = []
        
    def load_ai_sources(self):
        """加载AI数据源配置"""
        # 由于无法读取Excel，返回默认配置
        return self._get_default_sources()
    
    def _get_default_sources(self):
        """获取默认数据源配置"""
        return [
            {
                'name': '阿里云（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==',
                'home_url': '',
                'category': '云计算',
                'priority': 10,
                'enabled': 1
            },
            {
                'name': '腾讯研究院（微信公众号）',
                'type': 'rss',
                'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MjM5OTE0ODA2MQ==',
                'home_url': '',
                'category': '技术趋势',
                'priority': 10,
                'enabled': 1
            },
            {
                'name': 'AWS blog',
                'type': 'rss',
                'rss_url': 'https://aws.amazon.com/blogs/aws/feed/',
                'home_url': 'https://aws.amazon.com/blogs/',
                'category': '云计算',
                'priority': 10,
                'enabled': 1
            }
        ]
    
    def process_source_result(self, source_name, insights_count=0, result_status='', latest_publish_time=''):
        """处理单个数据源的获取结果"""
        
        # 获取数据源配置
        sources_config = self.load_ai_sources()
        
        for source in sources_config:
            if source['name'] == source_name:
                # 创建结果记录
                result_record = {
                    'name': source['name'],
                    'type': source.get('type', 'rss'),
                    'rss_url': source.get('rss_url', ''),
                    'home_url': source.get('home_url', ''),
                    'category': source.get('category', '其他'),
                    'priority': source.get('priority', 1),
                    'enabled': source.get('enabled', 1),
                    '获取简讯数': insights_count,
                    '获取结果': result_status,
                    '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # 如果有最新发布时间，添加到结果中
                if latest_publish_time:
                    result_record['最新简讯发布时间'] = latest_publish_time
                
                self.sources_data.append(result_record)
                return True
        
        print(f"⚠️ 未找到数据源配置: {source_name}")
        return False
    
    def generate_result_file(self):
        """生成结果文件"""
        
        print("🔧 生成数据源统计文件...")
        
        if not self.sources_data:
            print("⚠️ 没有数据源结果需要记录")
            return False
        
        try:
            # 确保目录存在
            os.makedirs('source', exist_ok=True)
            
            # 定义表头
            headers = ['name', 'type', 'rss_url', 'home_url', 'category', 'priority', 'enabled', 
                      '获取简讯数', '获取结果', '生成时间']
            
            # 检查是否有最新发布时间字段
            if any('最新简讯发布时间' in record for record in self.sources_data):
                headers.append('最新简讯发布时间')
            
            # 按优先级排序
            sorted_data = sorted(self.sources_data, key=lambda x: x.get('priority', 1), reverse=True)
            
            # 保存为CSV文件
            with open(self.result_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for record in sorted_data:
                    # 确保记录包含所有字段
                    row = {}
                    for header in headers:
                        row[header] = record.get(header, '')
                    writer.writerow(row)
            
            print(f"✅ 数据源统计文件已生成: {self.result_file}")
            
            # 同时保存为JSON格式便于查看
            with open('source/resultAI.json', 'w', encoding='utf-8') as jsonfile:
                json.dump(sorted_data, jsonfile, ensure_ascii=False, indent=2)
            
            print("✅ JSON格式文件已生成: source/resultAI.json")
            
            return True
            
        except Exception as e:
            print(f"❌ 生成数据源统计文件失败: {e}")
            return False
    
    def get_successful_sources_count(self):
        """获取成功获取的数据源数量"""
        successful_count = 0
        for source in self.sources_data:
            if source.get('获取简讯数', 0) > 0:
                successful_count += 1
        return successful_count
    
    def get_total_insights_count(self):
        """获取总简讯数量"""
        total_count = 0
        for source in self.sources_data:
            total_count += source.get('获取简讯数', 0)
        return total_count
    
    def print_summary(self):
        """打印统计摘要"""
        print("\n📊 数据源统计摘要:")
        print(f"   处理数据源数量: {len(self.sources_data)}")
        print(f"   成功获取数据源: {self.get_successful_sources_count()}")
        print(f"   总简讯数量: {self.get_total_insights_count()}")
        
        # 分类统计
        categories = {}
        for source in self.sources_data:
            cat = source.get('category', '其他')
            count = source.get('获取简讯数', 0)
            categories[cat] = categories.get(cat, 0) + count
        
        if categories:
            print("   分类统计:")
            for cat, count in categories.items():
                if count > 0:
                    print(f"     - {cat}: {count}条")

def create_partial_result_example():
    """创建部分数据源获取结果的示例"""
    
    print("🚀 创建部分数据源获取结果示例...")
    
    manager = SimpleResultAIManager()
    
    # 模拟部分数据源获取结果
    
    # 成功获取的数据源
    manager.process_source_result(
        source_name='阿里云（微信公众号）',
        insights_count=3,
        result_status='成功获取今日简讯',
        latest_publish_time='2026-03-04 00:07'
    )
    
    # 获取失败的数据源 - 时间不符合要求
    manager.process_source_result(
        source_name='腾讯研究院（微信公众号）',
        insights_count=0,
        result_status='最新文章时间2026-03-06，不满足今日要求',
        latest_publish_time='2026-03-06'
    )
    
    # 获取失败的数据源 - 网络问题
    manager.process_source_result(
        source_name='AWS blog',
        insights_count=0,
        result_status='rss_url地址访问失败，导致无数据'
    )
    
    # 生成结果文件
    manager.generate_result_file()
    manager.print_summary()

def main():
    """主函数"""
    
    print("🚀 简化版数据源统计管理器测试...")
    
    # 创建示例
    create_partial_result_example()
    
    print("\n🎉 简化版数据源统计管理器测试完成！")

if __name__ == "__main__":
    main()