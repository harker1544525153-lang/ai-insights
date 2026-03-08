#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据源RSS地址可访问性
"""

import json
import requests
import time

def test_rss_accessibility():
    """测试RSS地址可访问性"""
    
    print("=" * 80)
    print("数据源RSS地址可访问性测试")
    print("=" * 80)
    
    # 读取数据源配置文件
    try:
        with open('source/resultAI.json', 'r', encoding='utf-8') as f:
            data_sources = json.load(f)
        print("✅ 成功读取数据源配置文件")
    except Exception as e:
        print(f"❌ 读取数据源文件失败: {e}")
        return
    
    # 测试每个数据源的RSS URL
    accessible_count = 0
    total_count = len(data_sources)
    
    for source in data_sources:
        source_name = source['name']
        rss_url = source.get('rss_url', '')
        
        if not rss_url or rss_url.strip() == '':
            print(f"❌ {source_name}: RSS URL为空")
            continue
        
        try:
            # 设置请求头，模拟浏览器访问
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # 发送HEAD请求测试可访问性（更快）
            response = requests.head(rss_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {source_name}: 可访问 (状态码: {response.status_code})")
                accessible_count += 1
            else:
                print(f"❌ {source_name}: 不可访问 (状态码: {response.status_code})")
            
            # 避免请求过于频繁
            time.sleep(0.5)
            
        except requests.exceptions.Timeout:
            print(f"❌ {source_name}: 请求超时")
        except requests.exceptions.ConnectionError:
            print(f"❌ {source_name}: 连接错误")
        except Exception as e:
            print(f"❌ {source_name}: 错误 - {e}")
    
    # 统计结果
    print("\n" + "=" * 80)
    print(f"📊 测试结果统计:")
    print(f"   总数据源数量: {total_count}")
    print(f"   可访问数据源: {accessible_count}")
    print(f"   不可访问数据源: {total_count - accessible_count}")
    print(f"   可访问率: {accessible_count/total_count*100:.1f}%")
    
    if accessible_count / total_count >= 0.8:
        print("✅ RSS地址可访问性良好")
    elif accessible_count / total_count >= 0.5:
        print("⚠️ RSS地址可访问性一般")
    else:
        print("❌ RSS地址可访问性较差")
    
    print("=" * 80)

if __name__ == "__main__":
    test_rss_accessibility()