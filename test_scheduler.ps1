# scheduler.bat 测试脚本
Write-Host "========================================" -ForegroundColor Green
Write-Host "scheduler.bat 功能测试" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# 检查scheduler.bat文件是否存在
if (-not (Test-Path "scheduler.bat")) {
    Write-Host "❌ 错误: scheduler.bat文件不存在" -ForegroundColor Red
    exit 1
}

Write-Host "✅ scheduler.bat文件存在" -ForegroundColor Green

# 检查logs目录
if (Test-Path "logs") {
    Write-Host "✅ logs目录已存在" -ForegroundColor Green
    $logFiles = Get-ChildItem "logs\scheduler_*.log" -ErrorAction SilentlyContinue
    if ($logFiles) {
        Write-Host "📁 现有日志文件:" -ForegroundColor Cyan
        $logFiles | ForEach-Object { Write-Host "   - $($_.Name)" -ForegroundColor White }
    } else {
        Write-Host "ℹ️  logs目录为空" -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️  logs目录不存在" -ForegroundColor Yellow
}

# 测试直接运行cmd执行scheduler.bat
Write-Host ""
Write-Host "🚀 开始测试scheduler.bat执行..." -ForegroundColor Cyan

# 使用cmd执行scheduler.bat
$process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c scheduler.bat" -Wait -PassThru -NoNewWindow

Write-Host "✅ scheduler.bat执行完成，退出代码: $($process.ExitCode)" -ForegroundColor Green

# 检查是否生成了新的日志文件
Write-Host ""
Write-Host "🔍 检查新生成的日志文件..." -ForegroundColor Cyan

if (Test-Path "logs") {
    $newLogFiles = Get-ChildItem "logs\scheduler_*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($newLogFiles) {
        Write-Host "✅ 发现新的日志文件: $($newLogFiles.Name)" -ForegroundColor Green
        Write-Host "📄 日志文件路径: $($newLogFiles.FullName)" -ForegroundColor White
        
        # 显示日志文件内容（前20行）
        Write-Host ""
        Write-Host "📋 日志文件内容（前20行）:" -ForegroundColor Cyan
        try {
            $logContent = Get-Content $newLogFiles.FullName -Head 20
            $logContent | ForEach-Object { Write-Host "   $_" -ForegroundColor White }
        }
        catch {
            Write-Host "❌ 无法读取日志文件" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ 未发现新的日志文件" -ForegroundColor Red
    }
} else {
    Write-Host "❌ logs目录不存在，scheduler.bat可能执行失败" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "测试完成" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green