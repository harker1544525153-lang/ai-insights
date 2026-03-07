#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions环境测试脚本
用于验证在自动化环境中系统的运行情况
"""

import sys
import os
import pandas as pd
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment():
    """测试环境依赖和基本功能"""
    print("🔧 开始GitHub Actions环境测试")
    
    # 测试Python环境
    print(f"🐍 Python版本: {sys.version}")
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 测试依赖包
    try:
        import pandas as pd
        print("✅ pandas 可用")
    except ImportError as e:
        print(f"❌ pandas 导入失败: {e}")
        return False
    
    try:
        import feedparser
        print("✅ feedparser 可用")
    except ImportError as e:
        print(f"❌ feedparser 导入失败: {e}")
        return False
    
    # 测试数据源文件
    try:
        sources_file = "source/AI_sources.xlsx"
        if os.path.exists(sources_file):
            df = pd.read_excel(sources_file)
            print(f"✅ 数据源文件加载成功: {len(df)} 条记录")
        else:
            print(f"❌ 数据源文件不存在: {sources_file}")
            return False
    except Exception as e:
        print(f"❌ 数据源文件读取失败: {e}")
        return False
    
    # 测试输出目录
    output_dir = "result"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 创建输出目录: {output_dir}")
    
    # 生成测试文件
    test_content = f"""# AI简讯测试文件

## 测试时间
- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 环境: GitHub Actions测试

## 测试结果
✅ 环境依赖检查通过
✅ 数据源文件可用
✅ 输出目录准备就绪

## 下一步
系统已准备好在GitHub Actions中运行自动化任务
"""
    
    test_file = os.path.join(output_dir, "test_github_actions.md")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"📄 生成测试文件: {test_file}")
    print("🎉 GitHub Actions环境测试完成！")
    return True

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)