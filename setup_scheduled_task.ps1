# AI简讯自动更新定时任务设置脚本
# 此脚本将创建两个定时任务：
# 1. 每天8:00自动更新AI简讯
# 2. 每天8:30自动更新AI简讯

Write-Host "========================================" -ForegroundColor Green
Write-Host "AI简讯自动更新定时任务设置" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

# 检查是否以管理员权限运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "❌ 错误: 请以管理员权限运行此脚本" -ForegroundColor Red
    Write-Host "右键点击PowerShell，选择'以管理员身份运行'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ 检测到管理员权限" -ForegroundColor Green

# 脚本目录和批处理文件路径
$scriptDir = $PSScriptRoot
$batchFile = Join-Path $scriptDir "auto_update_news.bat"

# 检查批处理文件是否存在
if (-not (Test-Path $batchFile)) {
    Write-Host "❌ 错误: 未找到自动更新脚本 $batchFile" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 找到自动更新脚本: $batchFile" -ForegroundColor Green

# 定时任务配置
$tasks = @(
    @{
        Name = "AI简讯自动更新-08:00"
        Description = "每天8:00自动获取AI简讯并更新到GitHub"
        TriggerTime = "08:00"
    },
    @{
        Name = "AI简讯自动更新-08:30"
        Description = "每天8:30自动获取AI简讯并更新到GitHub"
        TriggerTime = "08:30"
    }
)

# 创建定时任务
foreach ($task in $tasks) {
    $taskName = $task.Name
    $taskDescription = $task.Description
    $triggerTime = $task.TriggerTime
    
    Write-Host "\n正在设置定时任务: $taskName" -ForegroundColor Cyan
    
    # 检查是否已存在同名任务
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "⚠️  任务已存在，先删除旧任务..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }
    
    # 创建触发器（每天指定时间运行）
    $trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime
    
    # 创建操作（运行批处理文件）
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$batchFile`"" -WorkingDirectory $scriptDir
    
    # 创建设置（确保任务在用户登录时运行）
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    # 注册定时任务
    try {
        $newTask = Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Trigger $trigger -Action $action -Settings $settings -RunLevel Highest
        
        Write-Host "✅ 定时任务创建成功: $taskName" -ForegroundColor Green
        Write-Host "   描述: $taskDescription" -ForegroundColor Gray
        Write-Host "   时间: 每天 $triggerTime" -ForegroundColor Gray
        Write-Host "   脚本: $batchFile" -ForegroundColor Gray
    }
    catch {
        Write-Host "❌ 定时任务创建失败: $taskName" -ForegroundColor Red
        Write-Host "   错误: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "\n========================================" -ForegroundColor Green
Write-Host "定时任务设置完成" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

Write-Host "\n📋 已创建的定时任务:" -ForegroundColor Cyan
Write-Host "   • AI简讯自动更新-08:00 (每天8:00运行)" -ForegroundColor White
Write-Host "   • AI简讯自动更新-08:30 (每天8:30运行)" -ForegroundColor White

Write-Host "\n🔍 查看定时任务状态:" -ForegroundColor Cyan
Write-Host "   1. 打开'任务计划程序'" -ForegroundColor White
Write-Host "   2. 任务计划程序库 -> AI简讯自动更新-08:00/AI简讯自动更新-08:30" -ForegroundColor White

Write-Host "\n⚡ 立即测试定时任务:" -ForegroundColor Cyan
Write-Host "   PowerShell: Start-ScheduledTask -TaskName 'AI简讯自动更新-08:00'" -ForegroundColor White
Write-Host "   或直接运行: .\auto_update_news.bat" -ForegroundColor White

Write-Host "\n📝 日志文件位置:" -ForegroundColor Cyan
Write-Host "   $scriptDir\auto_update.log" -ForegroundColor White

Write-Host "\n🎯 定时任务将在下次系统启动后自动运行" -ForegroundColor Green