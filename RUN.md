# Where to Run From - Quantum Pulse Project

**Working directory**: `c:\Users\User\Documents\quantum fi`

All commands below are run from this folder (the project root).

---

## 1. Install Dependencies (once)

```powershell
cd "c:\Users\User\Documents\quantum fi"
pip install -r requirements.txt
```

---

## 2. Streamlit App (interactive UI)

**From**: Project root `quantum fi`

```powershell
cd "c:\Users\User\Documents\quantum fi"
python -m streamlit run app.py
```

Or double-click **`run_app.bat`** in File Explorer.

- App opens at: http://localhost:8501
- Stop: `Ctrl+C` in the terminal

---

## 3. Pulse Comparison (generates plot)

**From**: Project root `quantum fi`

```powershell
cd "c:\Users\User\Documents\quantum fi"
python pulse_comparison.py
```

- Creates `pulse_comparison.png` in the same folder
- Prints energy and leakage stats for all 7 pulse types

---

## 4. Quantum Pulse Test (simulation + plot)

**From**: Project root `quantum fi`

```powershell
cd "c:\Users\User\Documents\quantum fi"
python test_pulse_quantum.py
```

- Creates `quantum_pulse_test_results.png`
- Prints quantum evolution and efficiency for 6 pulse types

---

## 5. Unit Tests

**From**: Project root `quantum fi`

```powershell
cd "c:\Users\User\Documents\quantum fi"
python test_pulses_unit.py
```

- Runs 4 unit tests (no extra output files)

---

## Quick Reference

| What           | Command                               | Output                          |
|----------------|----------------------------------------|---------------------------------|
| Streamlit app  | `python -m streamlit run app.py`       | Browser at localhost:8501       |
| Pulse comparison | `python pulse_comparison.py`         | pulse_comparison.png            |
| Quantum test   | `python test_pulse_quantum.py`         | quantum_pulse_test_results.png  |
| Unit tests     | `python test_pulses_unit.py`           | Pass/fail in terminal           |
| HTML Report    | `python export_report.py`              | report_YYYYMMDD_HHMMSS.html     |
| Qiskit Export  | `python export_qiskit_waveform.py`     | phi_pulses.npz                  |
| Manifest       | `python create_manifest.py`            | reproduce_manifest.json         |

---

## From VS Code / Cursor

1. Open the `quantum fi` folder as your workspace
2. Open a terminal (Ctrl+`)
3. Run any command above – the terminal is already in the project root
