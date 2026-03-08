#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复RSS URL token参数问题
确保RSS URL包含完整的token参数
"""

import pandas as pd
import os

def fix_rss_url_token():
    """修复RSS URL token参数问题"""
    
    print("开始修复RSS URL token参数问题...")
    
    # 文件路径
    ai_sources_file = "source/AI_sources.xlsx"
    resultai_file = "source/resultAI.csv"
    
    # 检查文件是否存在
    if not os.path.exists(ai_sources_file):
        print(f"错误: 文件不存在: {ai_sources_file}")
        return False
    
    if not os.path.exists(resultai_file):
        print(f"错误: 文件不存在: {resultai_file}")
        return False
    
    try:
        # 读取AI_sources.xlsx文件
        df_sources = pd.read_excel(ai_sources_file)
        print(f"成功加载 {len(df_sources)} 个数据源")
        
        # 读取resultAI.csv文件
        df_resultai = pd.read_csv(resultai_file)
        print(f"成功加载 {len(df_resultai)} 条resultAI记录")
        
        # 创建正确的RSS URL映射（包含完整token）
        rss_url_mapping = {
            '阿里云（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMyIsInR5cGUiOiJyc3MifQ.jD9i4ptS7kVD4xAlCly_pQN4E2DMnk1h0brfzOJA1lM',
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
        
        # 修复resultAI.csv中的RSS URL
        fixed_count = 0
        for index, row in df_resultai.iterrows():
            source_name = row['name']
            
            # 检查是否需要修复
            if source_name in rss_url_mapping:
                correct_url = rss_url_mapping[source_name]
                current_url = row.get('rss_url', '')
                
                # 如果URL不匹配，进行修复
                if current_url != correct_url and correct_url:
                    print(f"修复 {source_name}: {current_url} -> {correct_url}")
                    df_resultai.at[index, 'rss_url'] = correct_url
                    fixed_count += 1
        
        # 保存修复后的文件
        if fixed_count > 0:
            df_resultai.to_csv(resultai_file, index=False, encoding='utf-8')
            print(f"成功修复 {fixed_count} 个RSS URL")
            print(f"修复后的文件已保存: {resultai_file}")
        else:
            print("所有RSS URL都已正确，无需修复")
        
        # 显示修复前后的对比
        print("\n修复前后对比:")
        print("-" * 80)
        for source_name, correct_url in rss_url_mapping.items():
            if correct_url:  # 只显示有URL的数据源
                current_row = df_resultai[df_resultai['name'] == source_name]
                if not current_row.empty:
                    current_url = current_row.iloc[0]['rss_url']
                    status = "✅ 正确" if current_url == correct_url else "❌ 需要修复"
                    print(f"{source_name}: {status}")
                    if current_url != correct_url:
                        print(f"  当前: {current_url}")
                        print(f"  正确: {correct_url}")
        
        print("-" * 80)
        print("修复完成!")
        
        return True
        
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

def test_rss_url_fetch():
    """测试修复后的RSS URL是否能正常获取数据"""
    
    print("\n开始测试RSS URL数据获取...")
    
    try:
        import requests
        import feedparser
        
        # 测试阿里云的RSS URL
        test_url = 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMyIsInR5cGUiOiJyc3MifQ.jD9i4ptS7kVD4xAlCly_pQN4E2DMnk1h0brfzOJA1lM'
        
        print(f"测试URL: {test_url}")
        
        # 测试HTTP请求
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ HTTP请求成功")
            
            # 测试RSS解析
            feed = feedparser.parse(test_url)
            if feed.entries:
                print(f"✅ RSS解析成功，获取到 {len(feed.entries)} 篇文章")
                
                # 显示前3篇文章
                for i, entry in enumerate(feed.entries[:3], 1):
                    print(f"  {i}. {entry.title}")
                    print(f"     发布时间: {entry.published if hasattr(entry, 'published') else 'N/A'}")
                
                return True
            else:
                print("❌ RSS解析失败，无文章内容")
                return False
        else:
            print(f"❌ HTTP请求失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    # 执行修复
    if fix_rss_url_token():
        # 测试修复效果
        test_rss_url_fetch()
        
        print("\n" + "="*80)
        print("修复和测试完成!")
        print("现在可以重新运行 scheduler.bat 来获取完整的AI简讯数据")
        print("="*80)