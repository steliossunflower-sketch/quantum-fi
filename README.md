# Golden Ratio Quantum Pulse: A More Efficient Alternative

**Live app (shareable link):** [Add your Streamlit Cloud link here after deploy — see DEPLOY.md]

## 🔬 Discovery

This project demonstrates that a **Golden Ratio-based quantum pulse** uses **34% less energy** than standard Gaussian pulses while maintaining comparable spectral leakage properties. This finding could have significant implications for quantum computing efficiency.

## 📊 Key Results

- **Energy Efficiency**: Golden Ratio pulse uses 34.4% less total energy than Gaussian pulse
- **Energy Comparison**: 
  - Custom (Golden Ratio) Pulse: 36.95 energy units
  - Standard Gaussian Pulse: 56.34 energy units
- **Spectral Leakage**: Both pulses show minimal high-frequency leakage
- **Bandwidth**: Comparable frequency bandwidth characteristics

## 🎯 What This Means

In quantum computing, control pulses are used to manipulate qubits. More efficient pulses mean:
- Lower power consumption
- Reduced heating in quantum systems
- Potentially faster operations
- Better scalability for large quantum computers

## 🚀 Quick Start

**Run from**: `c:\Users\User\Documents\quantum fi` (project root)

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running

| Task | Command |
|------|---------|
| **Streamlit app** | Double-click `run_app.bat` or `python -m streamlit run app.py --server.port 8501` |
| **Pulse comparison** | `python pulse_comparison.py` |
| **Quantum tests** | `python test_pulse_quantum.py` |
| **Unit tests** | `python test_pulses_unit.py` |

**If ports are in use:** `run_app.bat` tries ports 8501–8520 automatically and opens your browser when the app is ready. If none are free, run `python -m streamlit run app.py --server.port 8521` and open http://localhost:8521 in your browser.

> See **RUN.md** for full run instructions.

### Pulse Comparison

```bash
python pulse_comparison.py
```

This will:
1. Generate both pulse shapes
2. Compare their spectral properties
3. Create visualization plots
4. Print detailed analysis results

### Output

The script generates:
- `pulse_comparison.png` - Side-by-side comparison plots showing time domain and frequency domain analysis

## 📈 Understanding the Results

### Time Domain Plot (Left)
Shows the pulse amplitude over time. Both pulses appear as smooth bell curves, but with different mathematical foundations.

### Frequency Domain Plot (Right)
Shows the Power Spectral Density (PSD) - where the pulse's energy is distributed across frequencies. Lower values (more negative dB) at high frequencies indicate less leakage, which is desirable.

## 🧮 The Math Behind It

The Golden Ratio pulse uses the formula:
```
A(t) = φ^(-t(t+1)/2)
```
where φ (phi) is the Golden Ratio ≈ 1.618

This creates a naturally smooth, energy-efficient pulse shape that decays gracefully at the edges.

## 📁 Project Structure

```
quantum-fi/
├── pulse_comparison.py    # Main analysis script
├── pulse_comparison.png   # Generated visualization
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔬 Technical Details

### Pulse Parameters
- **Duration**: 160 samples
- **Time Range**: -6 to 5 (mathematical units)
- **Normalization**: Both pulses normalized to peak amplitude of 1.0

### Analysis Methods
- **FFT**: Fast Fourier Transform for frequency analysis
- **PSD**: Power Spectral Density calculation in dB scale
- **Leakage Metrics**: High-frequency energy percentage analysis

## 🤝 Contributing

This is an open research project. Contributions, suggestions, and improvements are welcome!

## 📝 License

MIT License - See LICENSE file for details

## 👤 Author

Created as part of exploring quantum computing pulse optimization.

## 🔗 Related Resources

- [Qiskit Pulse Documentation](https://qiskit.org/documentation/apidoc/pulse.html)
- [Quantum Control Theory](https://en.wikipedia.org/wiki/Quantum_control)

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Note**: This research is exploratory and may benefit from further validation with actual quantum hardware.


