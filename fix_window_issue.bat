@echo off
REM ========================================
REM Fix CMD Window Flash Issue - English Version
REM ========================================

title Fix Window Flash Issue
mode con: cols=100 lines=30

echo ========================================
echo Fixing CMD Window Flash Issue
echo ========================================
echo.

REM Step 1: Check current directory
echo Step 1: Check current directory
echo Current directory: %cd%
echo.

REM Step 2: Check if key files exist
echo Step 2: Check key files
echo.

if exist scheduler.bat (
    echo [OK] scheduler.bat file exists
) else (
    echo [ERROR] scheduler.bat file not found
    goto error
)

if exist generate_fixed_news.py (
    echo [OK] generate_fixed_news.py file exists
) else (
    echo [ERROR] generate_fixed_news.py file not found
    goto error
)

if exist source\AI_sources.xlsx (
    echo [OK] source\AI_sources.xlsx file exists
) else (
    echo [ERROR] source\AI_sources.xlsx file not found
    goto error
)

echo.

REM Step 3: Check Python environment
echo Step 3: Check Python environment
echo.
python --version
if errorlevel 1 (
    echo [ERROR] Python environment check failed
    goto error
) else (
    echo [OK] Python environment is working
)

echo.

REM Step 4: Check Git environment
echo Step 4: Check Git environment
echo.
git --version
if errorlevel 1 (
    echo [ERROR] Git environment check failed
    goto error
) else (
    echo [OK] Git environment is working
)

echo.

REM Step 5: Create a simple test script
echo Step 5: Create simple test script
echo.

echo @echo off > test_simple.bat
echo title Simple Test Script >> test_simple.bat
echo echo Simple test script started >> test_simple.bat
echo echo Current directory: %%cd%% >> test_simple.bat
echo echo Press any key to exit... >> test_simple.bat
echo pause >> test_simple.bat

echo [OK] Created test_simple.bat
echo.

REM Step 6: Create scheduler with proper error handling
echo Step 6: Create fixed scheduler script
echo.

echo @echo off > scheduler_fixed_en.bat
echo title AI News Scheduler - Fixed Version >> scheduler_fixed_en.bat
echo mode con: cols=100 lines=30 >> scheduler_fixed_en.bat
echo. >> scheduler_fixed_en.bat

echo echo ======================================== >> scheduler_fixed_en.bat
echo echo AI News Scheduler Started >> scheduler_fixed_en.bat
echo echo Start time: %%date%% %%time%% >> scheduler_fixed_en.bat
echo echo ======================================== >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Force change to script directory >> scheduler_fixed_en.bat
echo cd /d "%%~dp0" >> scheduler_fixed_en.bat
echo echo Current directory: %%cd%% >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Create logs directory >> scheduler_fixed_en.bat
echo if not exist "%%~dp0logs" ( >> scheduler_fixed_en.bat
echo     mkdir "%%~dp0logs" >> scheduler_fixed_en.bat
echo     if errorlevel 1 ( >> scheduler_fixed_en.bat
echo         echo ERROR: Cannot create logs directory >> scheduler_fixed_en.bat
echo         goto error >> scheduler_fixed_en.bat
echo     ) >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo echo [OK] Logs directory ready >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Check Python >> scheduler_fixed_en.bat
echo python --version ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo ERROR: Python not found >> scheduler_fixed_en.bat
echo     goto error >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo echo [OK] Python check passed >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Check Git >> scheduler_fixed_en.bat
echo git --version ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo ERROR: Git not found >> scheduler_fixed_en.bat
echo     goto error >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo echo [OK] Git check passed >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Generate news >> scheduler_fixed_en.bat
echo echo Generating latest news... >> scheduler_fixed_en.bat
echo python generate_fixed_news.py ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo ERROR: News generation failed >> scheduler_fixed_en.bat
echo     goto error >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo echo [OK] News generation completed >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo REM Git operations >> scheduler_fixed_en.bat
echo echo Committing changes to Git... >> scheduler_fixed_en.bat
echo git add . ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo ERROR: Git add failed >> scheduler_fixed_en.bat
echo     goto error >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo git commit -m "Auto update AI news: %%date%% %%time%%" ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo WARNING: No changes to commit >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo git push origin main ^>nul 2^>^&1 >> scheduler_fixed_en.bat
echo if errorlevel 1 ( >> scheduler_fixed_en.bat
echo     echo ERROR: Git push failed >> scheduler_fixed_en.bat
echo     goto error >> scheduler_fixed_en.bat
echo ) >> scheduler_fixed_en.bat
echo echo [OK] Git operations completed >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat

echo echo ======================================== >> scheduler_fixed_en.bat
echo echo AI News Scheduler Completed Successfully! >> scheduler_fixed_en.bat
echo echo End time: %%date%% %%time%% >> scheduler_fixed_en.bat
echo echo ======================================== >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat
echo echo Press any key to close... >> scheduler_fixed_en.bat
echo pause ^>nul >> scheduler_fixed_en.bat
echo goto end >> scheduler_fixed_en.bat
echo. >> scheduler_fixed_en.bat

echo :error >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat
echo echo ======================================== >> scheduler_fixed_en.bat
echo echo AI News Scheduler Failed! >> scheduler_fixed_en.bat
echo echo Error time: %%date%% %%time%% >> scheduler_fixed_en.bat
echo echo ======================================== >> scheduler_fixed_en.bat
echo echo. >> scheduler_fixed_en.bat
echo echo Press any key to close... >> scheduler_fixed_en.bat
echo pause ^>nul >> scheduler_fixed_en.bat
echo. >> scheduler_fixed_en.bat

echo :end >> scheduler_fixed_en.bat

echo [OK] Created scheduler_fixed_en.bat
echo.

echo ========================================
echo Fixing completed!
echo ========================================
echo.
echo Created files:
echo 1. test_simple.bat - Simple window test
echo 2. scheduler_fixed_en.bat - Fixed scheduler script
echo.
echo Next steps:
echo 1. Double click test_simple.bat to test window display
echo 2. Double click scheduler_fixed_en.bat to test main function
echo.
echo Press any key to close this window...
pause >nul

goto end

:error
echo.
echo ========================================
echo Fixing failed!
echo ========================================
echo.
echo Please check the error messages above.
echo.
echo Press any key to close...
pause >nul

:end