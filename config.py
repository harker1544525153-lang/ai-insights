#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI简讯系统配置模块
"""

from datetime import datetime

def get_current_date():
    """获取当前日期"""
    return datetime.now().strftime('%Y-%m-%d')

def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime('%H:%M:%S')

def get_current_datetime():
    """获取当前日期时间"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 定时任务配置
SCHEDULE_CONFIG = {
    'morning_time': '08:00',  # 早上8:00
    'afternoon_time': '08:30'  # 早上8:30
}

# 数据源配置
DATA_SOURCES = {
    'excel_file': 'source/AI_sources.xlsx',
    'categories_file': 'categories.json',
    'output_dir': 'result'
}

# 输出配置
OUTPUT_CONFIG = {
    'html_template': 'result/index.html',
    'markdown_template': 'result/latest.md',
    'json_template': 'result/latest.json'
}

# 系统配置
SYSTEM_CONFIG = {
    'max_articles': 10,
    'test_mode': False,
    'auto_mode': True
}