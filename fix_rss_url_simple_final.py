#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复RSS URL问题 - 简单直接的方法
"""

import os

def fix_rss_url_simple():
    """简单修复RSS URL问题"""
    
    print("开始修复RSS URL问题...")
    
    # 文件路径
    resultai_file = "source/resultAI.csv"
    
    # 检查文件是否存在
    if not os.path.exists(resultai_file):
        print(f"错误: 文件不存在: {resultai_file}")
        return False
    
    try:
        # 尝试不同的编码方式读取文件
        encodings_to_try = ['utf-8-sig', 'gbk', 'gb2312', 'utf-8']
        
        content = None
        for enc in encodings_to_try:
            try:
                with open(resultai_file, 'r', encoding=enc) as f:
                    content = f.read()
                print(f"成功使用编码 {enc} 读取文件")
                break
            except UnicodeDecodeError:
                print(f"编码 {enc} 失败，尝试下一个...")
                continue
        
        if content is None:
            print("❌ 无法读取文件，所有编码尝试失败")
            return False
        
        # 正确的RSS URL映射（包含完整token）
        correct_rss_urls = {
            '阿里云（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ==?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMyIsInR5cGUiOiJyc3MifQ.jD9i4ptS7kVD4xAlCly_pQN4E2DMnk1h0brfzOJA1lM',
            '腾讯研究院（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MjM5OTE0ODA2MQ==',
            '新智元（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzI3MTA0MTk1MA==',
            '智东西（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzA4MTQ4NjQzMw==',
            '量子位（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzIzNjc1NzUzMw==',
            '云头条（微信公众号）': 'https://wechatrss.waytomaster.com/api/rss/MzI4OTc4MzI5OA=='
        }
        
        # 修复RSS URL
        fixed_count = 0
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            if line.strip():
                # 检查是否需要修复
                for source_name, correct_url in correct_rss_urls.items():
                    if source_name in line:
                        # 查找当前URL
                        current_url = 'https://wechatrss.waytomaster.com/api/rss/MzA4NjI4MzM4MQ=='
                        if current_url in line and correct_url not in line:
                            # 修复URL
                            new_line = line.replace(current_url, correct_url)
                            print(f"修复 {source_name}: {current_url} -> {correct_url}")
                            fixed_count += 1
                            line = new_line
                            break
                
                new_lines.append(line)
        
        # 保存修复后的文件
        if fixed_count > 0:
            # 使用UTF-8-BOM编码保存
            with open(resultai_file, 'w', encoding='utf-8-sig', newline='') as f:
                f.write('\n'.join(new_lines))
            
            print(f"成功修复 {fixed_count} 个RSS URL")
            print(f"修复后的文件已保存: {resultai_file}")
        else:
            print("所有RSS URL都已正确，无需修复")
        
        # 显示修复结果
        print("\n修复结果:")
        print("-" * 80)
        for source_name, correct_url in correct_rss_urls.items():
            if correct_url:
                # 检查修复结果
                found = False
                for line in new_lines:
                    if source_name in line and correct_url in line:
                        print(f"{source_name}: ✅ 正确")
                        found = True
                        break
                if not found:
                    print(f"{source_name}: ❌ 需要修复")
        
        print("-" * 80)
        print("修复完成!")
        
        return True
        
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

def test_rss_fetch():
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

def regenerate_news():
    """重新生成简讯"""
    
    print("\n开始重新生成简讯...")
    
    try:
        # 直接调用简讯生成函数
        import subprocess
        result = subprocess.run(['python', 'generate_fixed_news.py'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 简讯重新生成完成")
            # 显示部分输出
            for line in result.stdout.split('\n')[-10:]:
                if line.strip():
                    print(f"  {line}")
            return True
        else:
            print(f"❌ 简讯生成失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 简讯生成失败: {e}")
        return False

if __name__ == "__main__":
    # 执行修复
    if fix_rss_url_simple():
        # 测试修复效果
        if test_rss_fetch():
            # 重新生成简讯
            regenerate_news()
            
            print("\n" + "="*80)
            print("修复和测试完成!")
            print("现在可以查看最新的AI简讯，包含阿里云等数据源的完整内容")
            print("="*80)
        else:
            print("❌ RSS URL测试失败，请检查网络连接")
    else:
        print("❌ 修复失败，请检查文件权限")