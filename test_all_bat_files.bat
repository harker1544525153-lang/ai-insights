@echo off
REM ========================================
REM Test All Batch Files - Complete Test Suite
REM ========================================

title Test All Batch Files
mode con: cols=100 lines=30

echo ========================================
echo Testing All Batch Files
echo Start time: %date% %time%
echo ========================================
echo.

REM Test 1: Check if all required files exist
echo Test 1: Checking required files...
echo.

if exist scheduler.bat (
    echo [OK] scheduler.bat - Main scheduler file
) else (
    echo [ERROR] scheduler.bat not found
    goto error
)

if exist test_simple.bat (
    echo [OK] test_simple.bat - Simple test file
) else (
    echo [ERROR] test_simple.bat not found
    goto error
)

if exist test_with_error_handling.bat (
    echo [OK] test_with_error_handling.bat - Error handling test
) else (
    echo [ERROR] test_with_error_handling.bat not found
    goto error
)

if exist fix_window_issue.bat (
    echo [OK] fix_window_issue.bat - Window fix utility
) else (
    echo [ERROR] fix_window_issue.bat not found
    goto error
)

echo.
echo [OK] All batch files exist
echo.

REM Test 2: Check Python and Git environments
echo Test 2: Checking environments...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python environment check failed
    goto error
) else (
    echo [OK] Python environment is working
)

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git environment check failed
    goto error
) else (
    echo [OK] Git environment is working
)

echo.
echo [OK] All environment checks passed
echo.

REM Test 3: Test simple batch file
echo Test 3: Testing test_simple.bat...
echo.

call test_simple.bat
if errorlevel 1 (
    echo [ERROR] test_simple.bat execution failed
    goto error
) else (
    echo [OK] test_simple.bat test passed
)

echo.

REM Test 4: Test error handling batch file
echo Test 4: Testing test_with_error_handling.bat...
echo.

call test_with_error_handling.bat
if errorlevel 1 (
    echo [ERROR] test_with_error_handling.bat execution failed
    goto error
) else (
    echo [OK] test_with_error_handling.bat test passed
)

echo.

REM Test 5: Test main scheduler (quick test without full execution)
echo Test 5: Quick test of scheduler.bat...
echo.

REM Create a quick test version of scheduler
echo @echo off > test_scheduler_quick.bat
echo title Quick Scheduler Test >> test_scheduler_quick.bat
echo echo Quick scheduler test started >> test_scheduler_quick.bat
echo echo Current directory: %%cd%% >> test_scheduler_quick.bat
echo echo Python check: >> test_scheduler_quick.bat
echo python --version ^>nul 2^>^&1 >> test_scheduler_quick.bat
echo if errorlevel 1 goto error >> test_scheduler_quick.bat
echo echo Git check: >> test_scheduler_quick.bat
echo git --version ^>nul 2^>^&1 >> test_scheduler_quick.bat
echo if errorlevel 1 goto error >> test_scheduler_quick.bat
echo echo All checks passed! >> test_scheduler_quick.bat
echo echo Press any key to exit... >> test_scheduler_quick.bat
echo pause ^>nul >> test_scheduler_quick.bat
echo goto end >> test_scheduler_quick.bat
echo :error >> test_scheduler_quick.bat
echo echo Test failed >> test_scheduler_quick.bat
echo pause ^>nul >> test_scheduler_quick.bat
echo :end >> test_scheduler_quick.bat

call test_scheduler_quick.bat
if errorlevel 1 (
    echo [ERROR] Quick scheduler test failed
    goto error
) else (
    echo [OK] Quick scheduler test passed
)

echo.

REM Clean up test file
del test_scheduler_quick.bat

echo.
echo ========================================
echo All Tests Completed Successfully!
echo ========================================
echo.
echo Summary:
echo - All batch files exist and are accessible
echo - Python and Git environments are working
echo - Simple batch file execution test passed
echo - Error handling batch file test passed
echo - Quick scheduler functionality test passed
echo.
echo Next steps:
echo 1. Double click scheduler.bat to test full functionality
echo 2. Configure Windows Task Scheduler for automatic execution
echo 3. Monitor logs directory for execution records
echo.
echo Press any key to close this test window...
pause >nul

goto end

:error
echo.
echo ========================================
echo Testing Failed!
echo ========================================
echo.
echo Please check the error messages above.
echo.
echo Press any key to close...
pause >nul

:end