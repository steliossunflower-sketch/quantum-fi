@echo off
cd /d "%~dp0"
echo ============================================
echo   Phi Pulse vs All Quantum Pulse Types
echo ============================================
echo.

echo [1/6] Checking dependencies...
pip install -r requirements.txt --quiet 2>nul
echo.

echo [2/6] Generating pulse comparison plots...
python pulse_comparison.py
if errorlevel 1 (
    echo ERROR: pulse_comparison.py failed
    pause
    exit /b 1
)
echo.

echo [3/6] Running unit tests...
python test_pulses_unit.py
echo.

echo [4/6] Running quantum pulse test...
python test_pulse_quantum.py
echo.

echo [5/6] Opening website in browser...
start "" "%~dp0website\index.html"
echo.

echo [6/6] Starting Streamlit app...
echo    App: http://localhost:8765
echo    Press Ctrl+C to stop.
echo.
python -m streamlit run app.py --server.port 8876
if errorlevel 1 (
    echo Streamlit not found. Installing...
    pip install -r requirements.txt
    python -m streamlit run app.py --server.port 8876
)

pause
