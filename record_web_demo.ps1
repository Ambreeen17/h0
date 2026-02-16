# Web Dashboard Recording Guide
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Employee Dashboard Recording Guide" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "DASHBOARD IS RUNNING AT: http://localhost:5000" -ForegroundColor Yellow
Write-Host ""

Write-Host "RECORDING OPTIONS:" -ForegroundColor Green
Write-Host ""
Write-Host "1. WINDOWS GAME BAR (Built-in, Easiest):" -ForegroundColor White
Write-Host "   - Press Win+G to open Game Bar" -ForegroundColor Gray
Write-Host "   - Click Record button (or Win+Alt+R)" -ForegroundColor Gray
Write-Host "   - Open browser to http://localhost:5000" -ForegroundColor Gray
Write-Host "   - Show dashboard for 30-60 seconds" -ForegroundColor Gray
Write-Host "   - Press Win+Alt+R to stop" -ForegroundColor Gray
Write-Host ""
Write-Host "2. SCREEN RECORDING:" -ForegroundColor White
Write-Host "   - Open Game Bar: Win+G" -ForegroundColor Gray
Write-Host "   - Make sure browser is showing http://localhost:5000" -ForegroundColor Gray
Write-Host "   - Start recording" -ForegroundColor Gray
Write-Host ""
Write-Host "3. TAKE SCREENSHOTS:" -ForegroundColor White
Write-Host "   - Press Win+Shift+S for screenshot tool" -ForegroundColor Gray
Write-Host "   - Or run: .\capture_dashboard.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "DEMO CHECKLIST:" -ForegroundColor Yellow
Write-Host "  [ ] Show main dashboard with metrics" -ForegroundColor Gray
Write-Host "  [ ] Show Zone Status (Cloud/Local/Sync)" -ForegroundColor Gray
Write-Host "  [ ] Show task queues (Needs Action/Done)" -ForegroundColor Gray
Write-Host "  [ ] Mention auto-refresh every 2 seconds" -ForegroundColor Gray
Write-Host "  [ ] Show activity feed" -ForegroundColor Gray
Write-Host ""

Write-Host "Press Enter to open dashboard in browser..." -ForegroundColor Green
$null = Read-Host

Start-Process "http://localhost:5000"

Write-Host ""
Write-Host "Dashboard opened! Ready to record." -ForegroundColor Green
Write-Host "Videos save to: C:\Users\User\Videos\Captures\" -ForegroundColor Cyan
Write-Host ""
