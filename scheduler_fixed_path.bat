@echo off
REM ========================================
REM AI News Scheduler - Fixed Path Version
REM ========================================

title AI News Scheduler - Fixed Path
mode con: cols=100 lines=30

echo ========================================
echo AI News Scheduler Started
echo Start time: %date% %time%
echo ========================================
echo.

REM Force change to script directory with error checking
echo Changing to script directory...
cd /d "%~dp0"
if errorlevel 1 (
    echo ERROR: Cannot change to script directory
    goto error
)
echo Current directory: %cd%
echo.

REM Verify we are in the correct directory
if not exist generate_fixed_news.py (
    echo ERROR: generate_fixed_news.py not found in current directory
    echo Expected location: %cd%\generate_fixed_news.py
