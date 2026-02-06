"""
Streamlit App: Phi Pulse vs All Quantum Pulse Types
Visualizes Phi, Gaussian, DRAG, Square, Sinc, Raised Cosine, Gaussian Square.
"""

import matplotlib
matplotlib.use('Agg')
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.fft import fft, fftshift, fftfreq
import pandas as pd

try:
    from qiskit.quantum_info import Statevector, state_fidelity
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    class Statevector:
        def __init__(self, data):
            self.data = np.array(data) / np.linalg.norm(np.array(data))
        def __getitem__(self, i): return self.data[i]
    def state_fidelity(a, b):
        return np.abs(np.vdot(a.data, b.data))**2

import subprocess
import sys
import os

from pulse_comparison import (
    create_phi_pulse,
    create_gaussian_pulse,
    create_drag_pulse,
    create_square_pulse,
    create_sinc_pulse,
    create_raised_cosine_pulse,
    create_gaussian_square_pulse,
    compute_leakage_metrics,
)


def create_gaussian_custom(duration, sigma_divisor):
    sigma = duration / sigma_divisor
    t = np.linspace(-duration/2, duration/2, duration)
    s = np.exp(-(t**2) / (2 * sigma**2))
    return s / np.max(np.abs(s))


def create_drag_custom(duration, beta):
    sigma = duration / 5
    t = np.linspace(-duration/2, duration/2, duration)
    g = np.exp(-(t**2) / (2 * sigma**2))
    d = -t / (sigma**2) * g
    return (g + beta * d) / np.max(np.abs(g + beta * d))

st.set_page_config(page_title="Phi Pulse vs All Quantum Pulses", page_icon="🔬", layout="wide")

st.title("🔬 Phi Pulse vs All Quantum Pulse Types")
st.markdown("**Phi (Golden Ratio), Gaussian, DRAG, Square, Sinc, Raised Cosine, Gaussian Square**")
st.info("Sample rate: 1 GS/s. Time (ns), Frequency (GHz). All real comparisons.")

# Run tests & export — visible on entry
st.header("Run tests & export")
st.markdown("Run any test or export as soon as you open the app.")
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
act_col1, act_col2, act_col3, act_col4 = st.columns(4)
with act_col1:
    if st.button("Run Unit Tests", key="top_unit"):
        _r = subprocess.run(
            [sys.executable, os.path.join(_script_dir, "test_pulses_unit.py")],
            capture_output=True, text=True, cwd=_script_dir, timeout=30,
        )
        st.code(_r.stdout + _r.stderr or "(no output)", language="text")
        st.caption(f"Exit code: {_r.returncode}")
with act_col2:
    if st.button("Run Quantum Pulse Test", key="top_quantum"):
        _r = subprocess.run(
            [sys.executable, os.path.join(_script_dir, "test_pulse_quantum.py")],
            capture_output=True, text=True, cwd=_script_dir, timeout=60,
        )
        st.code(_r.stdout + _r.stderr or "(no output)", language="text")
        st.caption(f"Exit code: {_r.returncode}")
with act_col3:
    if st.button("Regenerate Pulse Comparison", key="top_regen"):
        _r = subprocess.run(
            [sys.executable, os.path.join(_script_dir, "pulse_comparison.py")],
            capture_output=True, text=True, cwd=_script_dir, timeout=30,
        )
        st.code(_r.stdout + _r.stderr or "(no output)", language="text")
        st.caption(f"Exit code: {_r.returncode}")
        if _r.returncode == 0:
            st.success("Plot saved. Refresh or reopen to see updated image.")
with act_col4:
    if st.button("Export Qiskit Waveform", key="top_export"):
        try:
            from export_qiskit_waveform import export_pulses_npz
            _cwd = os.getcwd()
            try:
                os.chdir(_script_dir)
                export_pulses_npz()
                st.success("Exported phi_pulses.npz (and waveform_*.npz if Qiskit available) to project folder.")
            finally:
                os.chdir(_cwd)
        except Exception as _e:
            _r = subprocess.run(
                [sys.executable, os.path.join(_script_dir, "export_qiskit_waveform.py")],
                capture_output=True, text=True, cwd=_script_dir, timeout=30,
            )
            out = (_r.stdout or "") + (_r.stderr or "")
            st.code(out or str(_e), language="text")
            st.caption("Exported to project folder if successful.")

st.sidebar.header("Controls")

st.sidebar.subheader("Pulse visibility (colored lines)")
st.sidebar.caption("Check/uncheck to show or hide pulses in plots")
show_phi = st.sidebar.checkbox("Phi (Golden Ratio)", True)
show_gaussian = st.sidebar.checkbox("Gaussian", True)
show_drag = st.sidebar.checkbox("DRAG", True)
show_square = st.sidebar.checkbox("Square", True)
show_sinc = st.sidebar.checkbox("Sinc", True)
show_raised_cosine = st.sidebar.checkbox("Raised Cosine", True)
show_gaussian_square = st.sidebar.checkbox("Gaussian Square", True)

st.sidebar.subheader("Duration & Phi")
duration = st.sidebar.slider("Duration (samples)", 10, 500, 160, 10)
t_min = st.sidebar.slider("Phi Time Start", -10.0, 0.0, -6.0, 0.5)
t_max = st.sidebar.slider("Phi Time End", 0.0, 10.0, 5.0, 0.5)

st.sidebar.subheader("Plot options (colored lines)")
line_width = st.sidebar.slider("Line width", 1.0, 5.0, 2.0, 0.5, help="Thickness of lines in time/frequency plots")
psd_ylim = st.sidebar.slider("PSD y-axis limit (dB)", -150, 20, -100, 10, help="Frequency plot vertical range")
target_angle_deg = st.sidebar.slider("Bloch: target angle (deg)", 0, 180, 90, 15)
bloch_show_all = st.sidebar.checkbox("Bloch: show all pulses (7 spheres)", True, help="Show Bloch sphere for every pulse type")
PULSE_NAMES = ["Phi (Golden Ratio)", "Gaussian", "DRAG", "Square", "Sinc", "Raised Cosine", "Gaussian Square"]
bloch_single_pulse = st.sidebar.selectbox("Bloch: single pulse (if not showing all)", PULSE_NAMES, index=0, disabled=bloch_show_all)

with st.sidebar.expander("Advanced: Gaussian & DRAG"):
    sigma_factor = st.slider("Gaussian sigma (duration / x)", 2, 15, 5, 1)
    drag_beta = st.slider("DRAG beta", 0.0, 0.5, 0.1, 0.05)

PHI = (1 + np.sqrt(5)) / 2
st.sidebar.write(f"**Phi**: {PHI:.6f}")

# IBM mode: compare Phi vs others in IBM hardware context (DRAG reference, 10-50 ns)
if "ibm_mode" not in st.session_state:
    st.session_state.ibm_mode = False
st.sidebar.subheader("IBM mode")
ibm_mode = st.sidebar.checkbox(
    "IBM mode",
    value=st.session_state.ibm_mode,
    help="Compare Phi vs others in terms of IBM hardware (DRAG reference, gate durations).",
)
st.session_state.ibm_mode = ibm_mode
if ibm_mode:
    st.sidebar.caption("Single-qubit gates on IBM hardware use Gaussian/DRAG at ~10–50 ns. Current duration (samples) = duration in ns at 1 GS/s.")

# Sample rate: 1 GS/s (typical for quantum hardware)
dt_ns = 1e-9  # seconds per sample


def compute_fft(samples, dt_sec=1e-9):
    """Compute FFT. Returns (freq_GHz, psd_dB) for 1 GS/s sample rate."""
    n = len(samples)
    yf = fft(samples)
    xf_Hz = fftfreq(n, dt_sec)
    yf_shifted = fftshift(yf)
    xf_shifted = fftshift(xf_Hz)
    xf_GHz = xf_shifted / 1e9
    psd = 20 * np.log10(np.abs(yf_shifted) + 1e-15)
    psd = psd - np.max(psd)
    return xf_GHz, psd


def simulate_quantum_evolution(pulse_samples, target_angle=np.pi/2):
    """
    Simulate quantum state evolution under the pulse.
    Returns the final quantum state and intermediate states for Bloch sphere visualization.
    """
    pulse_energy = np.sum(np.abs(pulse_samples)**2)
    pulse_duration = len(pulse_samples)
    effective_angle = target_angle * (pulse_energy / pulse_duration) / 0.5

    initial_state = np.array([1, 0], dtype=complex)
    states = [initial_state.copy()]

    num_steps = min(50, len(pulse_samples))
    step_indices = np.linspace(0, len(pulse_samples)-1, num_steps, dtype=int)

    cumulative_angle = 0
    for i in step_indices:
        partial_energy = np.sum(np.abs(pulse_samples[:i+1])**2)
        cumulative_angle = target_angle * (partial_energy / pulse_energy)

        cos_half = np.cos(cumulative_angle / 2)
        sin_half = np.sin(cumulative_angle / 2)
        rotation_matrix = np.array([
            [cos_half, -1j * sin_half],
            [-1j * sin_half, cos_half]
        ], dtype=complex)

        current_state = rotation_matrix @ initial_state
        states.append(current_state.copy())

    return states, effective_angle


def state_to_bloch_vector(state):
    """Convert quantum state to Bloch sphere coordinates (x, y, z)"""
    alpha = state[0]
    beta = state[1]
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2
    return np.array([x, y, z])


def plot_bloch_sphere_simple(states, title="Quantum State Evolution"):
    """Create a simplified Bloch sphere visualization"""
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='lightblue')

    ax.quiver(0, 0, 0, 1.2, 0, 0, color='r', arrow_length_ratio=0.1, linewidth=2)
    ax.quiver(0, 0, 0, 0, 1.2, 0, color='g', arrow_length_ratio=0.1, linewidth=2)
    ax.quiver(0, 0, 0, 0, 0, 1.2, color='b', arrow_length_ratio=0.1, linewidth=2)
    ax.text(1.3, 0, 0, 'X', fontsize=12, color='r')
    ax.text(0, 1.3, 0, 'Y', fontsize=12, color='g')
    ax.text(0, 0, 1.3, 'Z', fontsize=12, color='b')

    bloch_vectors = [state_to_bloch_vector(s) for s in states]
    bloch_vectors = np.array(bloch_vectors)

    ax.plot(bloch_vectors[:, 0], bloch_vectors[:, 1], bloch_vectors[:, 2],
            'o-', color='orange', linewidth=2, markersize=4, label='State Evolution')
    ax.scatter(*bloch_vectors[0], color='green', s=100, marker='o', label='Initial |0⟩')
    ax.scatter(*bloch_vectors[-1], color='red', s=100, marker='*', label='Final State')

    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend()

    return fig


# Build all pulses (use custom Gaussian/DRAG when params differ from defaults)
pulses = {
    'Phi (Golden Ratio)': create_phi_pulse(duration, t_min, t_max),
    'Gaussian': create_gaussian_custom(duration, sigma_factor),
    'DRAG': create_drag_custom(duration, drag_beta),
    'Square': create_square_pulse(duration),
    'Sinc': create_sinc_pulse(duration),
    'Raised Cosine': create_raised_cosine_pulse(duration),
    'Gaussian Square': create_gaussian_square_pulse(duration),
}
visibility = {
    'Phi (Golden Ratio)': show_phi,
    'Gaussian': show_gaussian,
    'DRAG': show_drag,
    'Square': show_square,
    'Sinc': show_sinc,
    'Raised Cosine': show_raised_cosine,
    'Gaussian Square': show_gaussian_square,
}
visible_pulses = {k: v for k, v in pulses.items() if visibility.get(k, True)}
energies = {name: np.sum(np.abs(p)**2) for name, p in pulses.items()}
phi_energy = energies.get('Phi (Golden Ratio)', energies[list(energies.keys())[0]])
time_ns = np.arange(duration)
colors = ['#e65100', '#1565c0', '#2e7d32', '#c62828', '#6a1b9a', '#00838f', '#f9a825']
name_to_color = {n: colors[i % len(colors)] for i, n in enumerate(pulses.keys())}

# Time domain plot
st.header("📈 Pulse Shapes (Time Domain)")
fig1, ax1 = plt.subplots(figsize=(12, 5))
for name, samples in visible_pulses.items():
    ax1.plot(time_ns, samples, label=name, color=name_to_color[name], linewidth=line_width, alpha=0.9)
ax1.set_xlabel('Time (ns)')
ax1.set_ylabel('Amplitude (normalized)')
ax1.set_title('Toggle pulses in sidebar to show/hide')
ax1.legend(loc='upper right', fontsize=9)
ax1.grid(True, alpha=0.3)
st.pyplot(fig1, width="stretch")
plt.close(fig1)

# Frequency domain plot
st.header("📡 Frequency Spectrum (Leakage)")
fig2, ax2 = plt.subplots(figsize=(12, 5))
for name, samples in visible_pulses.items():
    freqs, psd = compute_fft(samples, dt_ns)
    ax2.plot(freqs, psd, label=name, color=name_to_color[name], linewidth=line_width, alpha=0.9)
ax2.set_xlabel('Frequency (GHz)')
ax2.set_ylabel('Power Spectral Density (dB)')
ax2.set_ylim(psd_ylim, 5)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
st.pyplot(fig2, width="stretch")
plt.close(fig2)

# Bloch spheres - show all 7 pulse types (or single if unchecked)
st.header("🌐 Bloch Sphere - Quantum State Evolution")
st.markdown("Quantum state evolution under each pulse. Green = initial |0⟩, Red = final state.")
target_angle = np.radians(target_angle_deg)
pulses_for_bloch = pulses if bloch_show_all else {bloch_single_pulse: pulses[bloch_single_pulse]}
n_bloch = len(pulses_for_bloch)
cols = min(4, max(1, n_bloch))
bloch_cols = st.columns(cols)
for idx, (name, samples) in enumerate(pulses_for_bloch.items()):
    states, eff_angle = simulate_quantum_evolution(samples, target_angle)
    with bloch_cols[idx % cols]:
        fig_bloch = plot_bloch_sphere_simple(states, f"{name}")
        fig_bloch.set_size_inches(5, 5)
        st.pyplot(fig_bloch, width="stretch")
        plt.close(fig_bloch)
        st.caption(f"{name}: {np.degrees(eff_angle):.1f} deg (target {target_angle_deg})")

# Energy table
st.header("📊 Energy Comparison (Phi vs All)")
df_energy = pd.DataFrame([
    {'Pulse': name, 'Energy': f'{e:.2f}', 'Phi vs This': f'{100*(1 - phi_energy/e):.1f}%' if name != 'Phi (Golden Ratio)' and e > phi_energy else ('Phi uses more' if e < phi_energy else '-')}
    for name, e in energies.items()
])
st.dataframe(df_energy, width="stretch", hide_index=True)

# Leakage metrics
st.subheader("Leakage Metrics")
leakage_metrics = {n: compute_leakage_metrics(s, dt_ns) for n, s in pulses.items()}
df_leakage = pd.DataFrame([
    {'Pulse': name, 'High-freq Leakage %': f'{lk:.4f}', 'Bandwidth (-40dB) GHz': f'{bw:.4f}'}
    for name, (lk, bw) in leakage_metrics.items()
])
st.dataframe(df_leakage, width="stretch", hide_index=True)

# IBM mode: Phi vs others (IBM context)
if st.session_state.ibm_mode:
    st.header("Phi vs others (IBM context)")
    st.markdown("IBM single-qubit gates use Gaussian/DRAG at ~10–50 ns. Phi is compared above; lower energy and comparable leakage are favorable.")
    drag_energy = energies.get("DRAG", 1.0)
    duration_ns = duration  # 1 GS/s => 1 sample = 1 ns
    ibm_range_ok = 10 <= duration_ns <= 50
    ibm_rows = []
    for name, e in energies.items():
        lk, _ = leakage_metrics.get(name, (0, 0))
        if name == "Phi (Golden Ratio)":
            energy_vs_drag = "—"
            phi_savings = "—"
        else:
            pct_vs_drag = 100 * (e - drag_energy) / drag_energy if drag_energy else 0
            energy_vs_drag = f"{pct_vs_drag:+.1f}% vs DRAG"
            phi_savings = f"{100*(1 - phi_energy/e):.1f}%" if e > 0 else "—"
        in_range = "Yes" if ibm_range_ok else "No"
        # Simple IBM alignment score (0-100): lower energy vs DRAG and lower leakage = higher; duration in range adds bonus
        if drag_energy and drag_energy > 0:
            energy_penalty = min(50, max(0, 50 * (e / drag_energy - 1)))  # 0 if e <= drag, else up to 50
            leakage_penalty = min(40, lk * 10)
            alignment = max(0, min(100, 100 - energy_penalty - leakage_penalty + (10 if ibm_range_ok else 0)))
        else:
            alignment = 50
        ibm_rows.append({
            "Pulse": name,
            "Energy": f"{e:.2f}",
            "Energy vs DRAG": energy_vs_drag,
            "Phi savings vs this": phi_savings,
            "High-freq leakage %": f"{lk:.4f}",
            "Duration in 10–50 ns?": in_range,
            "IBM alignment (0–100)": f"{alignment:.0f}",
        })
    df_ibm = pd.DataFrame(ibm_rows)
    st.dataframe(df_ibm, width="stretch", hide_index=True)
    st.caption(f"Current duration: {duration_ns} ns. {'Within IBM single-qubit range (10–50 ns).' if ibm_range_ok else 'Outside 10–50 ns; adjust Duration (samples) in sidebar for IBM-like comparison.'}")
    st.download_button("Download IBM table (CSV)", df_ibm.to_csv(index=False), file_name=f"ibm_phi_vs_others_{duration_ns}ns.csv", mime="text/csv", key="dl_ibm_csv")

# CSV Download
st.subheader("Download Data")
data_dict = {'Time_ns': time_ns}
for name, p in pulses.items():
    data_dict[name.replace(' ', '_')] = p
df_csv = pd.DataFrame(data_dict)
st.download_button("Download CSV (all pulses)", df_csv.to_csv(index=False), file_name=f"all_pulses_{duration}.csv", mime="text/csv", key="dl_csv")

st.markdown("---")
st.markdown("Phi pulse: A(t) = φ^(-t(t+1)/2). Toggle pulse visibility in sidebar to compare.")
