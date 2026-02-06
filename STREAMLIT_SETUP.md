# Streamlit App Setup Guide

## Quick Start

### 1. Install Streamlit

```bash
pip install streamlit
```

Or if you want to install all dependencies at once:

```bash
pip install streamlit numpy matplotlib scipy pandas
```

### 2. Run the App

```bash
streamlit run app.py
```

The app will automatically open in your web browser at `http://localhost:8501`

## What the App Does

### Features

1. **Interactive Controls (Sidebar)**:
   - Duration slider (10-500 samples)
   - Toggle to show/hide Gaussian comparison
   - Time range controls for Golden Ratio pulse

2. **Visualizations**:
   - **Time Domain Plot**: Shows the pulse shape A(t) = φ^(-t(t+1)/2)
   - **Frequency Spectrum (FFT)**: Shows spectral leakage analysis
   - **Bloch Sphere**: 3D visualization of quantum state evolution

3. **Statistics**:
   - Energy comparison
   - Energy savings percentage
   - Pulse parameters

4. **Data Export**:
   - Download waveform data as CSV
   - Includes both Golden Ratio and Gaussian (if enabled)

## How to Use

1. **Adjust Parameters**:
   - Use the sidebar sliders to change pulse duration
   - Toggle Gaussian comparison on/off
   - Adjust time range for Golden Ratio pulse

2. **View Results**:
   - Watch the plots update in real-time
   - Compare energy usage between pulses
   - See quantum state evolution on Bloch sphere

3. **Export Data**:
   - Click "Download CSV" to save waveform data
   - Use the data for further analysis

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### "Qiskit not available" warning
This is optional! The app works without Qiskit, but Bloch sphere visualization uses a simplified version. For full features:
```bash
pip install qiskit
```

### App won't open in browser
- Check that port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`
- Or manually open: `http://localhost:8501`

### Plots not showing
- Make sure matplotlib is installed: `pip install matplotlib`
- Check browser console for errors (F12)

## Advanced Usage

### Run on Different Port
```bash
streamlit run app.py --server.port 8502
```

### Share with Others (Local Network)
```bash
streamlit run app.py --server.address 0.0.0.0
```
Then others can access via: `http://YOUR_IP:8501`

### Deploy Online
You can deploy to:
- **Streamlit Cloud** (free): [share.streamlit.io](https://share.streamlit.io)
- **Heroku**: Add Procfile and requirements.txt
- **AWS/GCP**: Use container services

## File Structure

```
quantum-fi/
├── app.py                    # Main Streamlit app
├── pulse_comparison.py       # Original analysis script
├── test_pulse_quantum.py     # Quantum simulation test
└── requirements.txt          # Dependencies
```

## Dependencies

Required:
- `streamlit` - Web app framework
- `numpy` - Numerical computations
- `matplotlib` - Plotting
- `scipy` - FFT and interpolation
- `pandas` - Data handling

Optional:
- `qiskit` - Enhanced Bloch sphere visualization

## Tips

1. **Start Simple**: Begin with default settings, then experiment
2. **Compare Pulses**: Enable Gaussian comparison to see the difference
3. **Export Data**: Download CSV to analyze in Excel/Python
4. **Share Results**: Take screenshots or share the app URL

## Next Steps

- Customize the app (add more features)
- Deploy online to share with others
- Add more pulse shapes for comparison
- Integrate with real quantum hardware APIs

Enjoy exploring your Golden Ratio quantum pulse! 🚀


