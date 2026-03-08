#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源未获取到今日简讯的原因分析报告
"""

import json
import datetime
import os

def analyze_data_source_issues():
    """分析数据源未获取到今日简讯的原因"""
    
    print("=" * 80)
    print("数据源未获取到今日简讯的原因分析报告")
    print("=" * 80)
    
    # 读取数据源统计文件
    try:
        with open('source/resultAI.json', 'r', encoding='utf-8') as f:
            data_sources = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取数据源文件: {e}")
        return
    
    # 统计信息
    total_sources = len(data_sources)
    successful_sources = sum(1 for source in data_sources if source.get("获取简讯数", 0) > 0)
    failed_sources = total_sources - successful_sources
    
    print(f"\n📊 数据源统计概览:")
    print(f"   总数据源数量: {total_sources}")
    print(f"   成功获取简讯: {successful_sources}")
    print(f"   未获取到简讯: {failed_sources}")
    print(f"   成功率: {successful_sources/total_sources*100:.1f}%")
    
    # 分析失败原因
    print(f"\n🔍 详细问题分析:")
    
    # 1. RSS URL问题
    rss_issues = []
    for source in data_sources:
        if source.get("获取简讯数", 0) == 0:
            rss_url = source.get("rss_url", "")
            if not rss_url or rss_url.strip() == "":
                rss_issues.append(f"   • {source['name']}: RSS URL为空")
            elif "wechatrss.waytomaster.com" in rss_url:
                # 检查微信公众号RSS URL是否完整
                if "?token=" not in rss_url:
                    rss_issues.append(f"   • {source['name']}: RSS URL缺少token参数")
    
    if rss_issues:
        print(f"\n❌ RSS URL问题 ({len(rss_issues)}个):")
        for issue in rss_issues:
            print(issue)
    
    # 2. 时间过滤问题
    time_issues = []
    current_date = datetime.datetime.now()
    
    for source in data_sources:
        latest_time = source.get("最新简讯发布时间", "")
        if latest_time:
            try:
                # 解析发布时间
                if "年" in latest_time and "月" in latest_time and "日" in latest_time:
                    date_part = latest_time.split(" ")[0]
                    year = int(date_part.split("年")[0])
                    month = int(date_part.split("年")[1].split("月")[0])
                    day = int(date_part.split("月")[1].split("日")[0])
                    publish_date = datetime.datetime(year, month, day)
                    
                    # 检查是否在时间过滤范围内
                    days_diff = (current_date - publish_date).days
                    if days_diff > 1:  # 超过1天
                        time_issues.append(f"   • {source['name']}: 最新文章发布于{days_diff}天前 ({latest_time})")
                        
            except Exception as e:
                time_issues.append(f"   • {source['name']}: 时间解析错误 ({latest_time})")
    
    if time_issues:
        print(f"\n⏰ 时间过滤问题 ({len(time_issues)}个):")
        for issue in time_issues:
            print(issue)
    
    # 3. 数据源配置问题
    config_issues = []
    for source in data_sources:
        if source.get("获取简讯数", 0) == 0:
            # 检查是否启用
            if source.get("enabled", "1") != "1":
                config_issues.append(f"   • {source['name']}: 数据源未启用")
            
            # 检查类型配置
            source_type = source.get("type", "")
            if not source_type:
                config_issues.append(f"   • {source['name']}: 类型配置为空")
    
    if config_issues:
        print(f"\n⚙️ 配置问题 ({len(config_issues)}个):")
        for issue in config_issues:
            print(issue)
    
    # 4. 成功的数据源分析
    successful_list = []
    for source in data_sources:
        if source.get("获取简讯数", 0) > 0:
            successful_list.append(f"   • {source['name']}: {source.get('获取简讯数', 0)}条简讯")
    
    if successful_list:
        print(f"\n✅ 成功获取简讯的数据源 ({len(successful_list)}个):")
        for item in successful_list:
            print(item)
    
    # 5. 根本原因总结
    print(f"\n📋 根本原因总结:")
    
    if rss_issues:
        print("   1. RSS URL问题:")
        print("      • 微信公众号RSS URL缺少token参数，导致无法获取内容")
        print("      • 部分数据源RSS URL为空或无效")
    
    if time_issues:
        print("   2. 时间过滤问题:")
        print("      • 数据源最新文章发布时间超过今天或上一个工作日")
        print("      • 时间过滤机制过于严格，可能过滤掉有效内容")
    
    if config_issues:
        print("   3. 配置问题:")
        print("      • 部分数据源未启用或配置不完整")
    
    # 6. 解决方案建议
    print(f"\n💡 解决方案建议:")
    
    print("   1. 修复RSS URL问题:")
    print("      • 为微信公众号RSS URL添加完整的token参数")
    print("      • 验证所有RSS URL的有效性")
    
    print("   2. 优化时间过滤机制:")
    print("      • 适当放宽时间过滤条件")
    print("      • 增加对周末时间的特殊处理")
    
    print("   3. 完善数据源配置:")
    print("      • 检查并启用所有有效数据源")
    print("      • 补充缺失的RSS URL")
    
    print("   4. 增加备用数据源:")
    print("      • 添加更多活跃的AI行业资讯源")
    print("      • 考虑使用API接口替代RSS")
    
    # 7. 具体修复步骤
    print(f"\n🔧 具体修复步骤:")
    
    print("   步骤1: 修复微信公众号RSS URL")
    print("      • 运行 fix_rss_url_simple_final.py 脚本")
    print("      • 验证URL格式: https://wechatrss.waytomaster.com/api/rss/...?token=...")
    
    print("   步骤2: 测试数据源有效性")
    print("      • 运行测试脚本验证RSS URL可访问性")
    print("      • 检查网络连接和API限制")
    
    print("   步骤3: 优化时间过滤逻辑")
    print("      • 修改 generate_fixed_news_corrected.py 中的时间判断逻辑")
    print("      • 增加对更多日期格式的支持")
    
    print("   步骤4: 更新数据源配置")
    print("      • 检查 AI_sources.xlsx 文件中的配置")
    print("      • 确保所有有效数据源都已启用")
    
    # 8. 当前状态评估
    print(f"\n📈 当前状态评估:")
    
    success_rate = successful_sources / total_sources * 100
    if success_rate >= 80:
        status = "良好"
        emoji = "✅"
    elif success_rate >= 50:
        status = "一般"
        emoji = "⚠️"
    else:
        status = "较差"
        emoji = "❌"
    
    print(f"   {emoji} 数据源获取成功率: {success_rate:.1f}% ({status})")
    print(f"   📅 数据统计时间: {data_sources[0].get('生成时间', '未知')}")
    print(f"   🔄 建议更新频率: 每日自动更新")
    
    print("\n" + "=" * 80)
    print("分析完成！建议按照上述解决方案逐步修复问题。")
    print("=" * 80)

def check_rss_url_status():
    """检查RSS URL状态"""
    
    print("\n🔗 RSS URL状态检查:")
    
    # 读取数据源
    try:
        with open('source/resultAI.json', 'r', encoding='utf-8') as f:
            data_sources = json.load(f)
    except Exception as e:
        print(f"无法读取数据源文件: {e}")
        return
    
    # 分析RSS URL
    wechat_sources = []
    valid_sources = []
    empty_sources = []
    
    for source in data_sources:
        rss_url = source.get("rss_url", "")
        if not rss_url or rss_url.strip() == "":
            empty_sources.append(source["name"])
        elif "wechatrss.waytomaster.com" in rss_url:
            if "?token=" in rss_url:
                valid_sources.append(source["name"])
            else:
                wechat_sources.append(source["name"])
        else:
            valid_sources.append(source["name"])
    
    print(f"   • 微信公众号RSS (需修复): {len(wechat_sources)}个")
    if wechat_sources:
        for name in wechat_sources:
            print(f"     - {name}")
    
    print(f"   • 有效RSS URL: {len(valid_sources)}个")
    print(f"   • 空RSS URL: {len(empty_sources)}个")
    if empty_sources:
        for name in empty_sources:
            print(f"     - {name}")

if __name__ == "__main__":
    analyze_data_source_issues()
    check_rss_url_status()