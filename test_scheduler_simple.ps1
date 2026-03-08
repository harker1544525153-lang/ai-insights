# scheduler.bat 简单测试脚本 - 避免编码问题
Write-Host "========================================"
Write-Host "scheduler.bat 双击执行测试"
Write-Host "========================================"

# 检查scheduler.bat是否存在
if (-not (Test-Path "scheduler.bat")) {
    Write-Host "错误: scheduler.bat文件不存在"
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host "scheduler.bat文件存在"

# 检查logs目录
if (-not (Test-Path "logs")) {
    Write-Host "logs目录不存在，将自动创建"
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
    if (-not (Test-Path "logs")) {
        Write-Host "错误: 无法创建logs目录"
        Read-Host "按Enter键退出"
        exit 1
    }
    Write-Host "logs目录创建成功"
} else {
    Write-Host "logs目录已存在"
}

Write-Host ""
Write-Host "检查环境配置..."

# 检查Python
$pythonResult = & python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python环境检查失败"
    goto error
}
Write-Host "Python环境检查通过: $pythonResult"

# 检查Git
$gitResult = & git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Git环境检查失败"
    goto error
}
Write-Host "Git环境检查通过: $gitResult"

Write-Host ""
Write-Host "========================================"
Write-Host "开始测试scheduler.bat执行..."
Write-Host "========================================"
Write-Host ""

# 执行scheduler.bat
$process = Start-Process -FilePath "scheduler.bat" -Wait -PassThru

if ($process.ExitCode -ne 0) {
    Write-Host "scheduler.bat执行失败，退出代码: $($process.ExitCode)"
    goto error
}

Write-Host ""
Write-Host "========================================"
Write-Host "scheduler.bat双击执行测试成功!"
Write-Host "========================================"

Write-Host ""
Write-Host "测试结果:"
Write-Host "- scheduler.bat文件存在"
Write-Host "- logs目录正常"
Write-Host "- 环境配置正常"
Write-Host "- 双击执行成功"

Write-Host ""
Write-Host "测试完成，窗口将在5秒后关闭..."
Start-Sleep -Seconds 5

exit

:error
Write-Host ""
Write-Host "========================================"
Write-Host "scheduler.bat双击执行测试失败"
Write-Host "========================================"

Write-Host ""
Write-Host "请检查:"
Write-Host "1. scheduler.bat文件是否存在"
Write-Host "2. Python和Git环境配置"
Write-Host "3. 网络连接状态"

Write-Host ""
Write-Host "窗口将在10秒后关闭..."
Start-Sleep -Seconds 10

exit 1