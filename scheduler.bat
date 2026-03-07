@echo off
REM ========================================
REM AI简讯定时任务调度器
REM 每天8:00和8:30自动执行
REM 程序或脚本: cmd.exe
REM 参数: /c "C:\Users\h604658591\Demo2\scheduler.bat"
REM 起始于: C:\Users\h604658591\Demo2
REM ========================================

REM 设置窗口标题
title AI简讯定时任务调度器

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 创建日志目录
if not exist logs mkdir logs

REM 获取当前时间用于日志文件名
for /f "tokens=1-3 delims=/" %%a in ('date /t') do set current_date=%%c%%a%%b
for /f "tokens=1-2 delims=:" %%a in ('time /t') do set current_time=%%a%%b
set log_file=logs\scheduler_%current_date%_%current_time%.log

REM 开始日志记录
echo ======================================== >> %log_file%
echo AI简讯定时任务调度器启动 >> %log_file%
echo 开始时间: %date% %time% >> %log_file%
echo ======================================== >> %log_file%

echo ========================================
echo AI简讯定时任务调度器
echo 开始时间: %date% %time%
echo ========================================

REM 检查Python是否可用
echo.
echo 🔍 检查Python环境...
python --version >> %log_file% 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH >> %log_file%
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH
    goto :error
)
echo ✅ Python环境检查通过 >> %log_file%
echo ✅ Python环境检查通过

REM 检查Git是否可用
echo.
echo 🔍 检查Git环境...
git --version >> %log_file% 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Git，请确保Git已安装并添加到PATH >> %log_file%
    echo ❌ 错误: 未找到Git，请确保Git已安装并添加到PATH
    goto :error
)
echo ✅ Git环境检查通过 >> %log_file%
echo ✅ Git环境检查通过

REM 1. 生成最新简讯
echo.
echo 🚀 开始生成最新简讯...
echo 🚀 开始生成最新简讯... >> %log_file%
python generate_fixed_news.py >> %log_file% 2>&1
if errorlevel 1 (
    echo ❌ 错误: 简讯生成失败 >> %log_file%
    echo ❌ 错误: 简讯生成失败
    goto :error
)
echo ✅ 简讯生成完成 >> %log_file%
echo ✅ 简讯生成完成

REM 2. 提交到Git
echo.
echo 📝 提交更改到Git...
echo 📝 提交更改到Git... >> %log_file%
git add . >> %log_file% 2>&1
if errorlevel 1 (
    echo ❌ 错误: Git添加文件失败 >> %log_file%
    echo ❌ 错误: Git添加文件失败
    goto :error
)

REM 获取当前时间用于提交信息
for /f "tokens=1-3 delims=/" %%a in ('date /t') do set commit_date=%%c-%%a-%%b
for /f "tokens=1-2 delims=:" %%a in ('time /t') do set commit_time=%%a:%%b

git commit -m "定时任务更新AI简讯: %commit_date% %commit_time%" >> %log_file% 2>&1
if errorlevel 1 (
    echo ⚠️ 警告: 没有新的更改需要提交，或提交失败 >> %log_file%
    echo ⚠️ 警告: 没有新的更改需要提交，或提交失败
    REM 继续执行，可能没有新内容
)
echo ✅ Git提交完成 >> %log_file%
echo ✅ Git提交完成

REM 3. 推送到GitHub
echo.
echo 📤 推送到GitHub...
echo 📤 推送到GitHub... >> %log_file%
git push origin main >> %log_file% 2>&1
if errorlevel 1 (
    echo ❌ 错误: Git推送失败 >> %log_file%
    echo ❌ 错误: Git推送失败
    goto :error
)
echo ✅ GitHub推送完成 >> %log_file%
echo ✅ GitHub推送完成

REM 4. 清理旧日志文件（保留最近7天的日志）
echo.
echo 🗑️ 清理旧日志文件...
echo 🗑️ 清理旧日志文件... >> %log_file%
forfiles /p "logs" /m "scheduler_*.log" /d -7 /c "cmd /c del @path" >> %log_file% 2>&1

echo.
echo ======================================== >> %log_file%
echo 🎉 AI简讯定时任务执行完成! >> %log_file%
echo 完成时间: %date% %time% >> %log_file%
echo ======================================== >> %log_file%

echo.
echo ========================================
echo 🎉 AI简讯定时任务执行完成!
echo 完成时间: %date% %time%
echo 日志文件: %log_file%
echo ========================================

REM 等待5秒后退出
timeout /t 5 /nobreak >nul

goto :end

:error
echo.
echo ======================================== >> %log_file%
echo ❌ 定时任务执行失败 >> %log_file%
echo 错误时间: %date% %time% >> %log_file%
echo ======================================== >> %log_file%

echo.
echo ========================================
echo ❌ 定时任务执行失败
echo 错误时间: %date% %time%
echo 请检查日志文件: %log_file%
echo ========================================

REM 等待10秒后退出
timeout /t 10 /nobreak >nul

:end
REM 正常退出