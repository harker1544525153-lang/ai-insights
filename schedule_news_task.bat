@echo off
REM AI简讯定时任务批处理文件
REM 用于Windows任务计划程序

REM 设置工作目录
cd /d "C:\Users\h604658591\Demo2"

REM 记录开始时间
echo [%date% %time%] 开始执行AI简讯定时任务 >> automation.log

REM 执行PowerShell自动化脚本
powershell -ExecutionPolicy Bypass -File "daily_news_automation.ps1"

REM 记录结束时间
echo [%date% %time%] AI简讯定时任务执行完成 >> automation.log

REM 如果执行成功，保持窗口打开以便查看结果
pause