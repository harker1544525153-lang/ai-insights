@echo off
REM ========================================
REM AI News Scheduler - Main Script
REM ========================================

title AI News Scheduler
mode con: cols=100 lines=30

echo ========================================
echo AI News Scheduler Started
echo Start time: %date% %time%
echo ========================================
echo.

REM Force change to script directory
cd /d "%~dp0"
echo Current directory: %cd%
echo.

REM Create logs directory
if not exist "%~dp0logs" (
    mkdir "%~dp0logs"
    if errorlevel 1 (
        echo ERROR: Cannot create logs directory
        goto error
    )
)
echo [OK] Logs directory ready
echo.

REM Set log file with timestamp
set current_date=%date:~0,4%%date:~5,2%%date:~8,2%
set current_time=%time:~0,2%%time:~3,2%
set current_time=%current_time: =0%
set log_file=%~dp0logs\scheduler_%current_date%_%current_time%.log

echo Log file: %log_file%
echo.

REM Start logging
echo ======================================== > "%log_file%"
echo AI News Scheduler Started >> "%log_file%"
echo Start time: %date% %time% >> "%log_file%"
echo Log file: %log_file% >> "%log_file%"
echo ======================================== >> "%log_file%"

REM Check Python environment
echo Checking Python environment...
echo Checking Python environment... >> "%log_file%"
python --version >> "%log_file%" 2>&1
if errorlevel 1 (
    echo ERROR: Python not found >> "%log_file%"
    echo ERROR: Python not found
    goto error
)
echo [OK] Python check passed >> "%log_file%"
echo [OK] Python check passed
echo.

REM Check Git environment
echo Checking Git environment...
echo Checking Git environment... >> "%log_file%"
git --version >> "%log_file%" 2>&1
if errorlevel 1 (
    echo ERROR: Git not found >> "%log_file%"
    echo ERROR: Git not found
    goto error
)
echo [OK] Git check passed >> "%log_file%"
echo [OK] Git check passed
echo.

REM Generate latest news
echo Generating latest news...
echo Generating latest news... >> "%log_file%"
python generate_fixed_news.py >> "%log_file%" 2>&1
if errorlevel 1 (
    echo ERROR: News generation failed >> "%log_file%"
    echo ERROR: News generation failed
    goto error
)
echo [OK] News generation completed >> "%log_file%"
echo [OK] News generation completed
echo.

REM Commit changes to Git
echo Committing changes to Git...
echo Committing changes to Git... >> "%log_file%"
git add . >> "%log_file%" 2>&1
if errorlevel 1 (
    echo ERROR: Git add failed >> "%log_file%"
    echo ERROR: Git add failed
    goto error
)

set commit_date=%date:~0,4%-%date:~5,2%-%date:~8,2%
set commit_time=%time:~0,2%:%time:~3,2%

git commit -m "Auto update AI news: %commit_date% %commit_time%" >> "%log_file%" 2>&1
if errorlevel 1 (
    echo WARNING: No changes to commit or commit failed >> "%log_file%"
    echo WARNING: No changes to commit or commit failed
)
echo [OK] Git commit completed >> "%log_file%"
echo [OK] Git commit completed
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo Pushing to GitHub... >> "%log_file%"
git push origin main >> "%log_file%" 2>&1
if errorlevel 1 (
    echo ERROR: Git push failed >> "%log_file%"
    echo ERROR: Git push failed
    goto error
)
echo [OK] GitHub push completed >> "%log_file%"
echo [OK] GitHub push completed
echo.

REM Clean old log files (keep last 7 days)
echo Cleaning old log files...
echo Cleaning old log files... >> "%log_file%"
forfiles /p "%~dp0logs" /m "scheduler_*.log" /d -7 /c "cmd /c echo Deleting old log: @path && del @path" >> "%log_file%" 2>&1

echo.
echo ======================================== >> "%log_file%"
echo AI News Scheduler Completed Successfully! >> "%log_file%"
echo End time: %date% %time% >> "%log_file%"
echo ======================================== >> "%log_file%"

echo.
echo ========================================
echo AI News Scheduler Completed Successfully!
echo End time: %date% %time%
echo ========================================
echo.
echo Task completed successfully!
echo Window will remain open for review.
echo Press any key to close...

REM Wait for user input before closing
pause >nul

goto end

:error
echo.
echo ======================================== >> "%log_file%"
echo AI News Scheduler Failed! >> "%log_file%"
echo Error time: %date% %time% >> "%log_file%"
echo ======================================== >> "%log_file%"

echo.
echo ========================================
echo AI News Scheduler Failed!
echo Error time: %date% %time%
echo ========================================
echo.
echo An error occurred during execution.
echo Please check the log file for details: %log_file%
echo Window will remain open for review.
echo Press any key to close...

REM Wait for user input before closing
pause >nul

:end