# AI简讯每日自动化脚本
# Windows定时任务专用

# 设置工作目录
Set-Location "C:\Users\h604658591\Demo2"

# 记录开始时间
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Output "[$timestamp] [INFO] 开始执行AI简讯自动化任务"
Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 开始执行AI简讯自动化任务"

# 1. 生成最新简讯
Write-Output "[$timestamp] [INFO] 开始生成AI简讯..."
Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 开始生成AI简讯..."

python generate_optimized_news.py

if ($LASTEXITCODE -eq 0) {
    Write-Output "[$timestamp] [INFO] AI简讯生成成功"
    Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] AI简讯生成成功"
} else {
    Write-Output "[$timestamp] [ERROR] AI简讯生成失败"
    Add-Content -Path "automation.log" -Value "[$timestamp] [ERROR] AI简讯生成失败"
    exit 1
}

# 2. 检查Git状态
Write-Output "[$timestamp] [INFO] 检查Git状态..."
Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 检查Git状态..."

$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Output "[$timestamp] [INFO] 检测到文件变更，准备提交到GitHub"
    Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 检测到文件变更，准备提交到GitHub"
    
    # 3. 添加所有变更文件
    git add .
    
    # 4. 提交变更
    $commitMessage = "每日AI简讯更新 - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMessage
    
    # 5. 推送到GitHub
    Write-Output "[$timestamp] [INFO] 推送到GitHub..."
    Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 推送到GitHub..."
    
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Output "[$timestamp] [INFO] 成功推送到GitHub"
        Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 成功推送到GitHub"
    } else {
        Write-Output "[$timestamp] [ERROR] GitHub推送失败"
        Add-Content -Path "automation.log" -Value "[$timestamp] [ERROR] GitHub推送失败"
        
        # 尝试强制推送
        Write-Output "[$timestamp] [INFO] 尝试强制推送..."
        Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 尝试强制推送..."
        
        git push -f origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Output "[$timestamp] [INFO] 强制推送成功"
            Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 强制推送成功"
        } else {
            Write-Output "[$timestamp] [ERROR] 强制推送也失败"
            Add-Content -Path "automation.log" -Value "[$timestamp] [ERROR] 强制推送也失败"
        }
    }
} else {
    Write-Output "[$timestamp] [INFO] 没有检测到文件变更，跳过GitHub提交"
    Add-Content -Path "automation.log" -Value "[$timestamp] [INFO] 没有检测到文件变更，跳过GitHub提交"
}

# 记录结束时间
$endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Output "[$endTime] [INFO] AI简讯自动化任务执行完成"
Add-Content -Path "automation.log" -Value "[$endTime] [INFO] AI简讯自动化任务执行完成"