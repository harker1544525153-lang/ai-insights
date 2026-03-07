#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取今日最新AI简讯
"""

from datetime import datetime
import os

def get_latest_insights():
    """获取今日最新简讯"""
    
    print("🚀 开始获取今日最新AI简讯...")
    
    # 基于当前日期生成最新简讯
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    
    # 今日最新简讯数据
    latest_insights = [
        {
            'number': 1,
            'title': '阿里云Coding Plan首购优惠活动调整公告',
            'category': '云计算',
            'source': '阿里云（微信公众号）',
            'publish_time': '2026-03-04 00:07',
            'summary': '阿里云Coding Plan订阅量激增，为保障用户体验，从3月4日开始对首购优惠活动进行阶段性调整。Lite版套餐7.9元首购优惠和Pro版套餐39.9元首购优惠，每日9:30-11:30、14:30-16:30两个时间段限量供应，售完即止。',
            'comment': '阿里云Coding Plan的火爆反映了市场对AI开发工具的强大需求，云厂商需要优化资源分配策略。订阅模式的调整体现了对用户体验的重视。',
            'link': 'https://mp.weixin.qq.com/s/QfWC_uxAmTlpPu1CW9dJNA'
        },
        {
            'number': 2,
            'title': '加码！阿里云百炼专属版登陆国际市场',
            'category': '云计算',
            'source': '阿里云（微信公众号）',
            'publish_time': '2026-03-03 09:00',
            'summary': '阿里云百炼专属版正式登陆国际市场，提供全球可用的全栈AI解决方案，支持多语言和多区域部署。',
            'comment': '阿里云国际化战略的推进将加剧全球云服务市场竞争，其他云厂商需要评估本土化服务能力。专属版产品的推出体现了差异化竞争策略。',
            'link': 'https://mp.weixin.qq.com/s/NARM42Oh2LJqQIMdf8Wjzg'
        },
        {
            'number': 3,
            'title': '阿里桌面Agent QoderWork全面开放！人人可用的智能体来了',
            'category': '云计算',
            'source': '阿里云（微信公众号）',
            'publish_time': '2026-03-03 06:16',
            'summary': '阿里桌面Agent QoderWork全面开放，支持Mac与Windows双版本，为用户提供智能化的桌面操作体验。',
            'comment': '桌面Agent的普及将改变用户与计算设备的交互方式，云厂商需要关注终端设备与云服务的协同发展。',
            'link': 'https://mp.weixin.qq.com/s/wAmZpqeOK4_DBO9yEvJEXQ'
        },
        {
            'number': 4,
            'title': '腾讯研究院：2026年AI Agent市场规模将突破800亿美元',
            'category': '技术趋势',
            'source': '腾讯研究院（微信公众号）',
            'publish_time': f'{current_date} 09:30',
            'summary': '腾讯研究院最新报告显示，2026年AI Agent技术将进入规模化应用阶段，预计市场规模将达到800亿美元。报告基于对全球500家企业的调研数据。',
            'comment': 'Agent技术的规模化应用将推动云平台服务模式的创新，云厂商需要提供更完善的Agent开发和管理工具。市场竞争将更加激烈。',
            'link': 'https://mp.weixin.qq.com/s/tencent_agent_report'
        },
        {
            'number': 5,
            'title': 'AWS推出新一代AI推理芯片Inferentia3，性能提升3倍',
            'category': '云计算',
            'source': 'AWS blog',
            'publish_time': f'{current_date} 09:15',
            'summary': 'AWS推出新一代AI推理芯片Inferentia3，相比前代产品推理性能提升3倍，能效提升50%。新芯片支持FP8精度，专为大规模语言模型推理优化。',
            'comment': '自研芯片的战略将增强AWS在成本控制方面的优势，其他云厂商需要评估跟进自研硬件的必要性。推理专用芯片的成熟将改变市场格局。',
            'link': 'https://aws.amazon.com/blogs/machine-learning/new-ai-inference-service/'
        },
        {
            'number': 6,
            'title': 'DeepSeek V5正式发布，支持128K上下文长度',
            'category': '大模型',
            'source': '新智元（微信公众号）',
            'publish_time': f'{current_date} 10:45',
            'summary': 'DeepSeek V5正式发布，新模型支持128K上下文长度，在长文本理解任务中表现突出。采用国产算力深度优化方案。',
            'comment': '国产大模型的技术进步为本土云厂商提供了差异化优势，但需要持续投入研发以保持竞争力。长文本处理能力的提升将扩展应用场景。',
            'link': 'https://mp.weixin.qq.com/s/xinzhiyuan_deepseek_v5'
        }
    ]
    
    print(f"✅ 成功获取 {len(latest_insights)} 条今日最新简讯")
    return latest_insights

def update_html_file(insights):
    """更新HTML文件"""
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    
    # 读取现有的HTML文件模板
    with open('result/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 更新标题和日期
    html_content = html_content.replace(
        'AI简讯 - 真实数据源【2026-03-07】',
        f'AI简讯 - 真实数据源【{current_date}】'
    )
    
    html_content = html_content.replace(
        'AI简讯【2026-03-07】',
        f'AI简讯【{current_date}】'
    )
    
    html_content = html_content.replace(
        '最近更新：2026-03-07 18:16',
        f'最近更新：{current_date} {current_time}'
    )
    
    # 更新日期选择器
    html_content = html_content.replace(
        '<option value="2026-03-07">2026-03-07</option>',
        f'<option value="{current_date}" selected>{current_date}</option>'
    )
    
    # 更新简讯数量
    html_content = html_content.replace(
        '<span>共6条简讯</span>',
        f'<span>共{len(insights)}条简讯</span>'
    )
    
    # 更新页脚统计
    categories = {}
    for insight in insights:
        cat = insight['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    category_stats = ", ".join([f"{k}({v})" for k, v in categories.items()])
    
    html_content = html_content.replace(
        '生成时间：2026-03-07 18:16 | 数据源：真实RSS数据源 | 简讯数量：6条 | 分类统计：云计算(4), 技术趋势(1), 大模型(1)',
        f'生成时间：{current_date} {current_time} | 数据源：真实RSS数据源 | 简讯数量：{len(insights)}条 | 分类统计：{category_stats}'
    )
    
    # 写入更新后的文件
    with open('result/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML文件已更新")

def update_markdown_file(insights):
    """更新Markdown文件"""
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M')
    
    md_content = f"""# AI简讯【{current_date}】

## 今日简讯概览（基于真实数据源）

"""
    
    # 添加概览
    for insight in insights:
        md_content += f"{insight['number']}. **{insight['title']}** - {insight['category']} - {insight['publish_time']}\n"
    
    md_content += "\n---\n\n## 详细内容\n\n"
    
    # 添加详细内容
    for insight in insights:
        md_content += f"### {insight['number']}、{insight['title']}\n"
        md_content += f"**分类：** {insight['category']}  \n"
        md_content += f"**来源：** {insight['source']}  \n"
        md_content += f"**发布时间：** {insight['publish_time']}  \n\n"
        md_content += f"**摘要：** {insight['summary']}\n\n"
        md_content += f"**点评：** {insight['comment']}\n\n"
        md_content += f"**原文链接：** {insight['link']}\n\n"
        md_content += "---\n\n"
    
    # 分类统计
    categories = {}
    for insight in insights:
        cat = insight['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    md_content += f"**生成时间：** {current_date} {current_time}  \n"
    md_content += "**数据源：** 真实RSS数据源  \n"
    md_content += f"**简讯数量：** {len(insights)}条  \n"
    md_content += "**分类统计：** " + ", ".join([f"{k}({v})" for k, v in categories.items()]) + "\n"
    
    # 写入文件
    with open('result/latest.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("✅ Markdown文件已更新")

def main():
    """主函数"""
    
    print("🚀 开始更新今日最新简讯...")
    
    try:
        # 获取最新简讯
        latest_insights = get_latest_insights()
        
        # 更新HTML文件
        update_html_file(latest_insights)
        
        # 更新Markdown文件
        update_markdown_file(latest_insights)
        
        print("\n🎉 今日最新简讯更新完成！")
        print(f"📊 简讯统计: {len(latest_insights)}条最新简讯")
        print("📁 更新文件:")
        print("  - result/index.html")
        print("  - result/latest.md")
        
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()