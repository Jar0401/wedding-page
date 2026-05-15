$folders = @(
    @{Path="C:\Users\Ren\Downloads"; Name="下载文件夹"},
    @{Path="C:\Users\Ren\Desktop"; Name="桌面"},
    @{Path="C:\Users\Ren\Documents"; Name="文档"},
    @{Path="C:\Windows\Temp"; Name="Windows 临时文件"},
    @{Path="C:\Users\Ren\AppData\Local\Temp"; Name="用户临时文件"},
    @{Path="C:\$Recycle.Bin"; Name="回收站"},
    @{Path="C:\Windows\SoftwareDistribution\Download"; Name="Windows 更新缓存"},
    @{Path="C:\ProgramData"; Name="程序数据"},
    @{Path="C:\Program Files"; Name="程序文件 (x64)"},
    @{Path="C:\Program Files (x86)"; Name="程序文件 (x86)"}
)

Write-Host "=".PadRight(60, "=") -ForegroundColor Cyan
Write-Host "C 盘空间占用扫描结果" -ForegroundColor Cyan
Write-Host "=".PadRight(60, "=") -ForegroundColor Cyan

$results = @()
foreach ($f in $folders) {
    if (Test-Path $f.Path) {
        $size = (Get-ChildItem $f.Path -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $results += [PSCustomObject]@{Size=$size; Name=$f.Name; Path=$f.Path}
    } else {
        $results += [PSCustomObject]@{Size=0; Name=$f.Name; Path=$f.Path}
    }
}

$results | Sort-Object Size -Descending | ForEach-Object {
    $sizeStr = if ($_.Size -gt 1GB) { "{0:N2} GB" -f ($_.Size / 1GB) } elseif ($_.Size -gt 1MB) { "{0:N2} MB" -f ($_.Size / 1MB) } else { "{0:N2} KB" -f ($_.Size / 1KB) }
    $exists = if (Test-Path $_.Path) { "" } else { " (不存在)" }
    Write-Host ($sizeStr.PadLeft(12) + "  |  " + $_.Name.PadRight(20) + $exists)
}

Write-Host ""
Write-Host "=".PadRight(60, "=") -ForegroundColor Yellow
Write-Host "AppData\Local 里的大文件夹 (>500MB)" -ForegroundColor Yellow
Write-Host "=".PadRight(60, "=") -ForegroundColor Yellow

$appData = "C:\Users\Ren\AppData\Local"
if (Test-Path $appData) {
    Get-ChildItem $appData -Directory | ForEach-Object {
        $s = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        if ($s -gt 500MB) {
            $sizeStr = if ($s -gt 1GB) { "{0:N2} GB" -f ($s / 1GB) } else { "{0:N2} MB" -f ($s / 1MB) }
            Write-Host ($sizeStr.PadLeft(12) + "  |  " + $_.Name)
        }
    }
}

Write-Host ""
Write-Host "扫描完成！" -ForegroundColor Green
