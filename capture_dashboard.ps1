# Quick Dashboard Screenshot Capture
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
$graphics = [System.Drawing.Graphics]::FromImage($bmp)

$timestamp = Get-Date -Format "HHmmss"
$filename = "demo_recording\screenshots\$timestamp-dashboard.png"

Write-Host "Capturing dashboard screenshot..." -ForegroundColor Cyan
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bmp.Save($filename)
$graphics.Dispose()
$bmp.Dispose()

Write-Host "Screenshot saved: $filename" -ForegroundColor Green
