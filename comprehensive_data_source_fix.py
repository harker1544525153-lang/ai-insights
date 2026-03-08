#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合数据源修复脚本
修复缺失的RSS URL和完善数据源配置
"""

import pandas as pd
import json
import os

def fix_missing_rss_urls():
    """补充缺失的RSS URL"""
    
    print("开始补充缺失的RSS URL...")
    
    # 读取数据源配置文件
    try:
        df = pd.read_excel('source/AI_sources.xlsx')
        print("✅ 成功读取AI_sources.xlsx")
    except Exception as e:
        print(f"❌ 读取数据源文件失败: {e}")
        return False
    
    # 定义缺失RSS URL的数据源及其对应的RSS URL
    missing_rss_mapping = {
        "GCP Blog": "https://cloud.google.com/feeds/google-cloud-blog-feed.xml",
        "AWS新闻": "https://press.aboutamazon.com/press-releases/rss/aws",
        "GCP新闻": "https://cloud.google.com/feeds/press-releases.xml",
        "NVIDIA新闻": "https://nvidianews.nvidia.com/rss.xml",
        "数据中心新闻": "https://www.datacenterdynamics.com/en/rss",
        "全球数据中心动态": "https://www.datacenterdynamics.com/en/rss"
    }
    
    # 修复缺失的RSS URL
    fixed_count = 0
    for index, row in df.iterrows():
        source_name = row['name']
        current_rss = row.get('rss_url', '')
        
        # 检查是否需要修复
        if pd.isna(current_rss) or str(current_rss).strip() == '':
            if source_name in missing_rss_mapping:
                new_rss = missing_rss_mapping[source_name]
                df.at[index, 'rss_url'] = new_rss
                print(f"✅ 为 {source_name} 添加RSS URL: {new_rss}")
                fixed_count += 1
            else:
                print(f"⚠️  {source_name} 的RSS URL为空，但未在修复映射中")
    
    # 保存修复后的文件
    if fixed_count > 0:
        df.to_excel('source/AI_sources.xlsx', index=False)
        print(f"✅ 已修复 {fixed_count} 个缺失的RSS URL")
        return True
    else:
        print("ℹ️ 没有需要修复的缺失RSS URL")
        return True

def fix_empty_type_configs():
    """修复类型配置为空的数据源"""
    
    print("\n开始修复类型配置为空的数据源...")
    
    # 读取数据源配置文件
    try:
        df = pd.read_excel('source/AI_sources.xlsx')
    except Exception as e:
        print(f"❌ 读取数据源文件失败: {e}")
        return False
    
    # 修复类型配置
    fixed_count = 0
    for index, row in df.iterrows():
        source_name = row['name']
        current_type = row.get('type', '')
        
        # 检查是否需要修复
        if pd.isna(current_type) or str(current_type).strip() == '':
            # 根据数据源名称推断类型
            if "新闻" in source_name or "动态" in source_name:
                new_type = "news"
            elif "Blog" in source_name or "blog" in source_name:
                new_type = "rss"
            else:
                new_type = "rss"  # 默认类型
            
            df.at[index, 'type'] = new_type
            print(f"✅ 为 {source_name} 设置类型: {new_type}")
            fixed_count += 1
    
    # 保存修复后的文件
    if fixed_count > 0:
        df.to_excel('source/AI_sources.xlsx', index=False)
        print(f"✅ 已修复 {fixed_count} 个类型配置")
        return True
    else:
        print("ℹ️ 没有需要修复的类型配置")
        return True

def add_more_data_sources():
    """添加更多活跃的AI行业资讯源"""
    
    print("\n开始添加更多活跃的AI行业资讯源...")
    
    # 读取现有数据源
    try:
        df = pd.read_excel('source/AI_sources.xlsx')
        existing_sources = set(df['name'].tolist())
    except Exception as e:
        print(f"❌ 读取数据源文件失败: {e}")
        return False
    
    # 新的数据源列表
    new_sources = [
        {
            "name": "OpenAI Blog",
            "type": "rss",
            "rss_url": "https://openai.com/blog/rss/",
            "home_url": "https://openai.com/blog",
            "category": "大模型",
            "priority": "10",
            "enabled": "1"
        },
        {
            "name": "Google AI Blog",
            "type": "rss",
            "rss_url": "https://ai.googleblog.com/feeds/posts/default",
            "home_url": "https://ai.googleblog.com",
            "category": "大模型",
            "priority": "10",
            "enabled": "1"
        },
        {
            "name": "Microsoft AI Blog",
            "type": "rss",
            "rss_url": "https://blogs.microsoft.com/ai/feed/",
            "home_url": "https://blogs.microsoft.com/ai",
            "category": "AI Agent",
            "priority": "10",
            "enabled": "1"
        },
        {
            "name": "Meta AI Blog",
            "type": "rss",
            "rss_url": "https://ai.meta.com/blog/rss/",
            "home_url": "https://ai.meta.com/blog",
            "category": "大模型",
            "priority": "10",
            "enabled": "1"
        },
        {
            "name": "AI News",
            "type": "rss",
            "rss_url": "https://artificialintelligence-news.com/feed/",
            "home_url": "https://artificialintelligence-news.com",
            "category": "技术趋势",
            "priority": "5",
            "enabled": "1"
        }
    ]
    
    # 添加新数据源
    added_count = 0
    for new_source in new_sources:
        if new_source["name"] not in existing_sources:
            # 创建新行并添加到DataFrame
            new_row = pd.DataFrame([new_source])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"✅ 添加新数据源: {new_source['name']}")
            added_count += 1
        else:
            print(f"ℹ️ 数据源已存在: {new_source['name']}")
    
    # 保存更新后的文件
    if added_count > 0:
        df.to_excel('source/AI_sources.xlsx', index=False)
        print(f"✅ 已添加 {added_count} 个新数据源")
        return True
    else:
        print("ℹ️ 没有需要添加的新数据源")
        return True

def verify_fix_results():
    """验证修复结果"""
    
    print("\n开始验证修复结果...")
    
    # 读取修复后的数据源文件
    try:
        df = pd.read_excel('source/AI_sources.xlsx')
        total_sources = len(df)
        
        # 统计修复结果
        empty_rss_count = sum(1 for rss in df['rss_url'] if pd.isna(rss) or str(rss).strip() == '')
        empty_type_count = sum(1 for type_val in df['type'] if pd.isna(type_val) or str(type_val).strip() == '')
        disabled_count = sum(1 for enabled in df['enabled'] if str(enabled) != '1')
        
        print(f"📊 修复后数据源统计:")
        print(f"   总数据源数量: {total_sources}")
        print(f"   空RSS URL数量: {empty_rss_count}")
        print(f"   空类型配置数量: {empty_type_count}")
        print(f"   未启用数据源数量: {disabled_count}")
        
        # 评估修复效果
        if empty_rss_count == 0 and empty_type_count == 0 and disabled_count == 0:
            print("✅ 所有数据源问题已修复！")
            return True
        else:
            print("⚠️ 部分问题仍需修复")
            if empty_rss_count > 0:
                print(f"   • 仍有 {empty_rss_count} 个空RSS URL")
            if empty_type_count > 0:
                print(f"   • 仍有 {empty_type_count} 个空类型配置")
            if disabled_count > 0:
                print(f"   • 仍有 {disabled_count} 个未启用数据源")
            return False
            
    except Exception as e:
        print(f"❌ 验证修复结果失败: {e}")
        return False

def main():
    """主修复流程"""
    
    print("=" * 80)
    print("综合数据源修复脚本")
    print("=" * 80)
    
    # 执行修复步骤
    steps = [
        ("补充缺失的RSS URL", fix_missing_rss_urls),
        ("修复类型配置", fix_empty_type_configs),
        ("添加更多数据源", add_more_data_sources),
        ("验证修复结果", verify_fix_results)
    ]
    
    all_success = True
    for step_name, step_func in steps:
        print(f"\n🔧 执行步骤: {step_name}")
        try:
            success = step_func()
            if not success:
                all_success = False
                print(f"❌ {step_name} 执行失败")
        except Exception as e:
            print(f"❌ {step_name} 执行出错: {e}")
            all_success = False
    
    # 总结修复结果
    print("\n" + "=" * 80)
    if all_success:
        print("🎉 数据源修复完成！")
        print("💡 建议下一步执行: python full_workflow.py 重新生成简讯")
    else:
        print("⚠️ 数据源修复部分完成，部分问题仍需手动处理")
    print("=" * 80)

if __name__ == "__main__":
    main()