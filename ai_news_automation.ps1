# AI简讯自动化脚本 - 新版本
# 支持从AI_sources.xlsx获取数据源

# 设置工作目录
Set-Location "C:\Users\h604658591\Demo2"

# 记录日志
function Write-Log {
    param($message, $level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$level] $message"
    Write-Host $logMessage
    Add-Content -Path "ai_news_automation.log" -Value $logMessage
}

Write-Log "开始执行AI简讯自动化任务（新版本）"

# 1. 检查依赖
Write-Log "检查Python依赖..."

try {
    # 检查pandas
    $pandasCheck = python -c "import pandas; print('pandas OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "安装pandas..." "WARNING"
        pip install --user pandas
    }
    
    # 检查feedparser
    $feedparserCheck = python -c "import feedparser; print('feedparser OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "安装feedparser..." "WARNING"
        pip install --user feedparser
    }
    
    # 检查beautifulsoup4
    $bs4Check = python -c "import bs4; print('bs4 OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "安装beautifulsoup4..." "WARNING"
        pip install --user beautifulsoup4
    }
    
    # 检查requests
    $requestsCheck = python -c "import requests; print('requests OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "安装requests..." "WARNING"
        pip install --user requests
    }
    
    Write-Log "Python依赖检查完成"
}
catch {
    Write-Log "依赖检查失败: $_" "ERROR"
}

# 2. 检查数据源文件
if (-not (Test-Path "AI_sources.xlsx")) {
    Write-Log "AI_sources.xlsx文件不存在，请检查数据源配置" "ERROR"
    exit 1
}

Write-Log "数据源文件检查通过"

# 3. 生成最新AI简讯
Write-Log "开始生成AI简讯..."
$startTime = Get-Date

python ai_news_system.py

if ($LASTEXITCODE -eq 0) {
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    Write-Log "AI简讯生成成功，耗时: $duration 秒"
} else {
    Write-Log "AI简讯生成失败" "ERROR"
    exit 1
}

# 4. 检查生成的文件
$requiredFiles = @("index.html", "resultAI.xlsx")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Log "生成的文件缺失: $file" "ERROR"
        exit 1
    }
}

Write-Log "所有必需文件生成完成"

# 5. 检查Git状态并上传到GitHub
Write-Log "检查Git状态..."
$gitStatus = git status --porcelain

if ($gitStatus) {
    Write-Log "检测到文件变更，准备提交到GitHub"
    
    # 添加所有变更文件
    git add .
    
    # 提交变更
    $commitMessage = "AI简讯自动更新 - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git commit -m $commitMessage
    
    # 推送到GitHub
    Write-Log "推送到GitHub..."
    
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "成功推送到GitHub"
    } else {
        Write-Log "GitHub推送失败，尝试强制推送..." "WARNING"
        
        git push -f origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "强制推送成功"
        } else {
            Write-Log "强制推送也失败" "ERROR"
        }
    }
} else {
    Write-Log "没有检测到文件变更，跳过GitHub提交"
}

# 6. 记录执行结果
$endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Log "AI简讯自动化任务执行完成"

# 生成执行报告
$report = "AI简讯自动化任务执行报告`n"
$report += "==========================`n"
$report += "执行时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$report += "工作目录: $(Get-Location)`n`n"
$report += "生成文件:`n"
$report += "- index.html (AI简讯网页)`n"
$report += "- resultAI.xlsx (处理结果)`n"
$report += "- ai_news_automation.log (执行日志)`n`n"
$report += "Git状态: $(if ($gitStatus) { '有变更' } else { '无变更' })`n"
$report += "Git提交: $(if ($gitStatus) { '已提交' } else { '未提交' })`n`n"
$report += "任务状态: 完成`n"

Add-Content -Path "execution_report.txt" -Value $report
Write-Log "执行报告已生成: execution_report.txt"

Write-Output "✅ AI简讯自动化任务执行完成！"