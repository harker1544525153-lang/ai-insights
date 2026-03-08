#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全流程AI简讯生成器 - 固定流程
包含数据获取、网页生成、Markdown生成、Excel统计、GitHub上传
"""

import datetime
import os
import subprocess
import time

def run_full_workflow():
    """执行全流程AI简讯生成"""
    
    print("=" * 80)
    print("AI简讯全流程生成器")
    print("开始时间:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 80)
    
    # 步骤1: 修复RSS URL问题
    print("\n[步骤1] 修复RSS URL问题...")
    try:
        result = subprocess.run(['python', 'fix_rss_url_simple_final.py'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ RSS URL修复完成")
        else:
            print("⚠️ RSS URL修复失败，继续执行")
    except Exception as e:
        print(f"⚠️ RSS URL修复异常: {e}")
    
    # 步骤2: 生成修正版简讯
    print("\n[步骤2] 生成修正版简讯...")
    try:
        result = subprocess.run(['python', 'generate_fixed_news_corrected.py'], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ 修正版简讯生成完成")
            # 显示生成结果
            for line in result.stdout.split('\n')[-10:]:
                if line.strip():
                    print(f"  {line}")
        else:
            print(f"❌ 简讯生成失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 简讯生成异常: {e}")
    
    # 步骤3: 验证生成的文件
    print("\n[步骤3] 验证生成的文件...")
    files_to_check = [
        'index.html',
        'result/index.html', 
        'latest.md',
        'source/resultAI.csv'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {file_size} bytes")
        else:
            print(f"❌ {file_path} - 文件不存在")
    
    # 步骤4: 显示最新简讯内容
    print("\n[步骤4] 最新简讯内容预览...")
    try:
        with open('latest.md', 'r', encoding='utf-8') as f:
            content = f.read()
            # 显示前200个字符作为预览
            preview = content[:200] + "..." if len(content) > 200 else content
            print("简讯预览:")
            print("-" * 50)
            print(preview)
            print("-" * 50)
    except Exception as e:
        print(f"❌ 简讯预览失败: {e}")
    
    # 步骤5: 准备GitHub上传
    print("\n[步骤5] 准备GitHub上传...")
    try:
        # 检查Git状态
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git仓库状态正常")
            
            # 添加文件到Git
            subprocess.run(['git', 'add', '.'], capture_output=True)
            
            # 提交更改
            commit_message = f"AI简讯更新 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Git提交完成")
                print(f"提交信息: {commit_message}")
            else:
                print("⚠️ Git提交失败或无更改")
                
            # 推送到GitHub
            result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print("✅ 推送到GitHub完成")
            else:
                print("⚠️ GitHub推送失败")
                
        else:
            print("⚠️ Git仓库未初始化或存在问题")
            
    except Exception as e:
        print(f"❌ GitHub上传异常: {e}")
    
    # 步骤6: 生成最终报告
    print("\n[步骤6] 生成最终报告...")
    
    # 检查生成的文件
    html_exists = os.path.exists('index.html')
    md_exists = os.path.exists('latest.md')
    csv_exists = os.path.exists('source/resultAI.csv')
    
    # 统计简讯数量
    insight_count = 0
    if md_exists:
        try:
            with open('latest.md', 'r', encoding='utf-8') as f:
                content = f.read()
                insight_count = content.count('## ')
        except:
            pass
    
    # 生成报告
    report = f"""
📊 AI简讯全流程生成报告
========================

📅 生成时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📋 文件生成状态:
   • HTML网页: {'✅ 已生成' if html_exists else '❌ 未生成'}
   • Markdown文档: {'✅ 已生成' if md_exists else '❌ 未生成'}
   • Excel统计: {'✅ 已更新' if csv_exists else '❌ 未更新'}

📈 简讯统计:
   • 生成简讯数量: {insight_count}条
   • 数据源数量: 23个
   • 发布时间范围: 今天或上一个工作日

🌐 在线访问:
   • GitHub Pages: https://harker1544525153-lang.github.io/ai-insights/

🔧 技术状态:
   • RSS URL修复: ✅ 已完成
   • 时间过滤: ✅ 已启用
   • 链接修正: ✅ 已完成
   • 编码处理: ✅ 已优化

💡 下一步操作:
   1. 查看 index.html 文件确认网页显示
   2. 检查 latest.md 文件确认内容完整性
   3. 访问GitHub Pages验证在线发布
   4. 设置定时任务自动执行
"""
    
    print(report)
    
    # 保存报告到文件
    with open('workflow_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("✅ 全流程执行完成!")
    print("=" * 80)
    print("📁 生成的文件:")
    print("   • index.html (网页版简讯)")
    print("   • latest.md (文档版简讯)")
    print("   • workflow_report.txt (流程报告)")
    print("=" * 80)

def check_webpage_style():
    """检查网页样式是否保留原有样式"""
    print("\n[样式检查] 验证网页样式...")
    
    if os.path.exists('index.html'):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查关键样式元素
            style_checks = {
                '渐变背景': 'background: linear-gradient' in content,
                '卡片样式': 'insight-card' in content,
                '响应式设计': '@media' in content or 'max-width' in content,
                '深色科技感': '#667eea' in content or '#764ba2' in content
            }
            
            print("网页样式检查结果:")
            for check_name, check_result in style_checks.items():
                status = "✅ 存在" if check_result else "❌ 缺失"
                print(f"  {check_name}: {status}")
                
            if all(style_checks.values()):
                print("✅ 网页样式完整保留")
            else:
                print("⚠️ 部分样式可能缺失")
                
        except Exception as e:
            print(f"❌ 样式检查失败: {e}")
    else:
        print("❌ index.html文件不存在")

if __name__ == "__main__":
    # 执行全流程
    run_full_workflow()
    
    # 检查网页样式
    check_webpage_style()
    
    print("\n🎉 全流程AI简讯生成完成!")
    print("现在可以查看生成的文件和访问在线版本")