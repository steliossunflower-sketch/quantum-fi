# PowerShell script to run the Streamlit app
Set-Location $PSScriptRoot
Write-Host "Starting Golden Ratio Quantum Pulse Visualizer..." -ForegroundColor Green
Write-Host ""

# Check if Streamlit is available
$streamlitOk = $false
try {
    python -m streamlit --version | Out-Null
    $streamlitOk = $true
} catch {
    # ignore
}
if (-not $streamlitOk) {
    Write-Host "Streamlit not found. Installing..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt --quiet
    Write-Host ""
}

# Try ports 8501 through 8505 until one works
$ports = 8501..8505
$started = $false
foreach ($port in $ports) {
    Write-Host "Trying port $port..." -ForegroundColor Cyan
    $p = Start-Process -FilePath "python" -ArgumentList "-m", "streamlit", "run", "app.py", "--server.port", $port, "--server.headless", "false" -PassThru -NoNewWindow -Wait
    if ($p.ExitCode -eq 0) {
        $started = $true
        break
    }
    if ($port -eq 8505) {
        Write-Host ""
        Write-Host "All ports 8501-8505 are in use. Close another app using these ports, or run:" -ForegroundColor Yellow
        Write-Host "  python -m streamlit run app.py --server.port 8506" -ForegroundColor White
        Write-Host "then open http://localhost:8506 in your browser." -ForegroundColor White
        break
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
