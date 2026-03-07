#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复resultAI.csv中的RSS URL，使其与AI_sources.xlsx保持一致
"""

import pandas as pd
import os

def fix_rss_urls():
    """修复RSS URL不一致问题"""
    
    # 文件路径
    ai_sources_file = "source/AI_sources.xlsx"
    resultai_file = "source/resultAI.csv"
    
    print("🔧 开始修复RSS URL不一致问题...")
    
    # 检查文件是否存在
    if not os.path.exists(ai_sources_file):
        print(f"❌ 文件不存在: {ai_sources_file}")
        return False
    
    if not os.path.exists(resultai_file):
        print(f"❌ 文件不存在: {resultai_file}")
        return False
    
    try:
        # 读取AI_sources.xlsx
        print("📖 正在读取AI_sources.xlsx...")
        ai_sources_df = pd.read_excel(ai_sources_file)
        
        # 读取resultAI.csv
        print("📖 正在读取resultAI.csv...")
        resultai_df = pd.read_csv(resultai_file)
        
        # 创建RSS URL映射字典
        rss_url_mapping = {}
        for _, row in ai_sources_df.iterrows():
            name = row.get('name', '')
            rss_url = row.get('rss_url', '')
            if name and pd.notna(rss_url) and rss_url:
                rss_url_mapping[name] = rss_url
        
        print(f"📊 从AI_sources.xlsx中读取到{len(rss_url_mapping)}个RSS URL")
        
        # 更新resultAI.csv中的RSS URL
        updated_count = 0
        for idx, row in resultai_df.iterrows():
            name = row['name']
            if name in rss_url_mapping:
                correct_rss_url = rss_url_mapping[name]
                current_rss_url = row['rss_url']
                
                # 检查是否需要更新
                if pd.isna(current_rss_url) or current_rss_url != correct_rss_url:
                    resultai_df.at[idx, 'rss_url'] = correct_rss_url
                    updated_count += 1
                    print(f"✅ 更新 {name} 的RSS URL")
                    print(f"   原URL: {current_rss_url}")
                    print(f"   新URL: {correct_rss_url}")
        
        # 保存更新后的文件
        if updated_count > 0:
            resultai_df.to_csv(resultai_file, index=False, encoding='utf-8-sig')
            print(f"\n🎉 成功更新了{updated_count}个RSS URL")
            print(f"📁 文件已保存: {resultai_file}")
        else:
            print("ℹ️ 所有RSS URL都已正确，无需更新")
        
        # 显示统计信息
        print("\n📊 数据源统计:")
        print(f"   总数据源数量: {len(resultai_df)}")
        print(f"   成功获取简讯: {len(resultai_df[resultai_df['获取结果'] == '成功获取今日简讯'])}")
        print(f"   获取失败: {len(resultai_df[resultai_df['获取结果'] == '获取失败'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {e}")
        return False

def create_sample_ai_sources():
    """创建示例AI_sources.xlsx文件（如果不存在）"""
    
    # 根据用户提供的数据源创建示例数据
    sample_data = [
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
            'category': '大模型',
            'priority': 10,
            'enabled': 1
        },
        {
            'name': '新智元（微信公众号）',
            'type': 'rss',
            'rss_url': 'https://wechatrss.waytomaster.com/api/rss/MzI3MTA0MTk1MA==',
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
            'category': '算力',
            'priority': 10,
            'enabled': 1
        },
        {
            'name': 'Azure Blog',
            'type': 'rss',
            'rss_url': 'https://azure.microsoft.com/en-us/blog/feed/',
            'home_url': 'https://azure.microsoft.com/en-us/blog/',
            'category': 'AI Agent',
            'priority': 10,
            'enabled': 1
        },
        {
            'name': 'NVIDIA blog',
            'type': 'rss',
            'rss_url': 'https://blogs.nvidia.com/feed/',
            'home_url': 'https://blogs.nvidia.com/',
            'category': '算力',
            'priority': 10,
            'enabled': 1
        }
    ]
    
    df = pd.DataFrame(sample_data)
    df.to_excel('source/AI_sources.xlsx', index=False)
    print("✅ 已创建示例AI_sources.xlsx文件")

if __name__ == "__main__":
    # 检查是否需要创建示例文件
    if not os.path.exists("source/AI_sources.xlsx"):
        print("📝 AI_sources.xlsx文件不存在，创建示例文件...")
        create_sample_ai_sources()
    
    # 修复RSS URL
    fix_rss_urls()