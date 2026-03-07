#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复resultAI.csv中的RSS URL，使其与AI_sources.xlsx保持一致
简化版本，不使用pandas
"""

import csv
import os

def fix_rss_urls():
    """修复RSS URL不一致问题"""
    
    # 文件路径
    ai_sources_file = "source/AI_sources.xlsx"
    resultai_file = "source/resultAI.csv"
    
    print("🔧 开始修复RSS URL不一致问题...")
    
    # 检查文件是否存在
    if not os.path.exists(resultai_file):
        print(f"❌ 文件不存在: {resultai_file}")
        return False
    
    # 根据用户提供的数据源创建正确的RSS URL映射
    rss_url_mapping = {
        '阿里云（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==',
        '腾讯研究院（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MjM5OTE0ODA2MQ==',
        '新智元（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzI3MTA0MTk1MA==',
        '智东西（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzA4MTQ4NjQzMw==',
        '量子位（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzIzNjc1NzUzMw==',
        '云头条（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzI4OTc4MzI5OA==',
        'AWS blog': 'https://aws.amazon.com/blogs/aws/feed/',
        'Azure Blog': 'https://azure.microsoft.com/en-us/blog/feed/',
        'NVIDIA blog': 'https://blogs.nvidia.com/feed/',
        'Azure 新闻': 'https://nvidianews.nvidia.com/rss.xml',
        'GCP Blog': '',
        'AWS新闻': '',
        'GCP新闻': '',
        'NVIDIA新闻': '',
        '数据中心新闻': '',
        '全球数据中心动态': '',
        'TechCrunch': 'https://techcrunch.com/tag/google/feed/',
        'VentureBeat': 'https://venturebeat.com/feed',
        'The Verge': 'https://www.theverge.com/rss/index.xml',
        'InfoQ AI': 'https://www.infoq.cn/feed',
        '36氪（AI频道）': 'https://36kr.com/feed',
        'IT之家AI': 'https://www.ithome.com/rss/',
        '阿里云开发者（微信公众号）': 'https://wechat2rss.xlab.app/feed/c74ed6db00cfbf16f2a048a165b4453f982681f0.xml'
    }
    
    try:
        # 读取resultAI.csv
        print("📖 正在读取resultAI.csv...")
        rows = []
        with open(resultai_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)
        
        # 更新RSS URL
        updated_count = 0
        for row in rows:
            name = row['name']
            if name in rss_url_mapping:
                correct_rss_url = rss_url_mapping[name]
                current_rss_url = row['rss_url']
                
                # 检查是否需要更新
                if current_rss_url != correct_rss_url:
                    row['rss_url'] = correct_rss_url
                    updated_count += 1
                    print(f"✅ 更新 {name} 的RSS URL")
                    print(f"   原URL: {current_rss_url}")
                    print(f"   新URL: {correct_rss_url}")
        
        # 保存更新后的文件
        if updated_count > 0:
            with open(resultai_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"\n🎉 成功更新了{updated_count}个RSS URL")
            print(f"📁 文件已保存: {resultai_file}")
        else:
            print("ℹ️ 所有RSS URL都已正确，无需更新")
        
        # 显示统计信息
        print("\n📊 数据源统计:")
        print(f"   总数据源数量: {len(rows)}")
        success_count = len([r for r in rows if r['获取结果'] == '成功获取今日简讯'])
        failed_count = len([r for r in rows if r['获取结果'] == '获取失败'])
        print(f"   成功获取简讯: {success_count}")
        print(f"   获取失败: {failed_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    fix_rss_urls()