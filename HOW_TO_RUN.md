# How to Run

> **Quick reference**: See `RUN.md` for all commands (Streamlit, pulse comparison, tests).

## Streamlit App - Quick Start

### Method 1: Double-Click (Easiest for Windows)

1. **Double-click `run_app.bat`** in your file explorer
2. The app will open automatically in your browser
3. If Streamlit isn't installed, it will install it first

### Method 2: Command Line (Windows)

Open PowerShell or Command Prompt in this folder and run:

```bash
python -m streamlit run app.py
```

Or use the batch file:
```bash
.\run_app.bat
```

### Method 3: PowerShell Script

Right-click `run_app.ps1` and select "Run with PowerShell"

Or in PowerShell:
```powershell
.\run_app.ps1
```

## If Streamlit Isn't Installed

The launcher scripts will automatically install it, or you can install manually:

```bash
pip install streamlit pandas
```

## Accessing the App

Once running, the app will be available at:
- **Local URL**: `http://localhost:8501`
- It should open automatically in your browser
- If not, copy the URL and paste it in your browser

## Stopping the App

- Press `Ctrl+C` in the terminal/command prompt
- Or close the terminal window

## Troubleshooting

### "streamlit is not recognized"
- Use: `python -m streamlit run app.py` instead of just `streamlit run app.py`
- Or install: `pip install streamlit`

### "ModuleNotFoundError"
- Install dependencies: `pip install streamlit pandas numpy matplotlib scipy`

### App doesn't open in browser
- Manually go to: `http://localhost:8501`
- Check if port 8501 is already in use
- Try a different port: `python -m streamlit run app.py --server.port 8502`

### Port already in use
- Kill the process using port 8501, or
- Use a different port: `python -m streamlit run app.py --server.port 8502`

## Running Anytime

Just double-click `run_app.bat` whenever you want to use the app!

The app will:
- ✅ Check if Streamlit is installed
- ✅ Install it if needed
- ✅ Start the app automatically
- ✅ Open in your browser

## What You'll See

1. **Sidebar** (left): Controls to adjust pulse parameters
2. **Main Area**: 
   - Pulse shape visualization
   - Frequency spectrum (FFT)
   - Bloch sphere (quantum state evolution)
   - Download CSV button

Enjoy exploring your Golden Ratio quantum pulse! 🚀


