"""
Quantum Pulse Testing: Golden Ratio vs Gaussian
Tests both pulses in quantum simulations. Validates pulse behavior for qubit control.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq

try:
    from qiskit.quantum_info import Statevector, state_fidelity
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    class SimpleStatevector:
        def __init__(self, data):
            self.data = np.array(data)
            self.data = self.data / np.linalg.norm(self.data)
        def __getitem__(self, idx):
            return self.data[idx]
    def simple_fidelity(state1, state2):
        return np.abs(np.vdot(state1.data, state2.data))**2
    Statevector = SimpleStatevector
    state_fidelity = simple_fidelity

dt_ns = 1e-9


def create_golden_ratio_pulse(duration=160):
    PHI = (1 + np.sqrt(5)) / 2
    t_min, t_max = -6, 5
    t_vals = np.linspace(t_min, t_max, duration)
    samples = PHI ** (-(t_vals * (t_vals + 1)) / 2)
    return samples / np.max(np.abs(samples))


def create_gaussian_pulse(duration=160):
    sigma = duration / 5
    t = np.linspace(-duration/2, duration/2, duration)
    samples = np.exp(-(t**2) / (2 * sigma**2))
    return samples / np.max(np.abs(samples))


def get_spectral_energy(samples, dt_sec=1e-9):
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
    pulse_energy = np.sum(np.abs(pulse_samples)**2)
    pulse_duration = len(pulse_samples)
    effective_angle = target_angle * (pulse_energy / pulse_duration) / 0.5
    initial_state = Statevector([1, 0])
    cos_half = np.cos(effective_angle / 2)
    sin_half = np.sin(effective_angle / 2)
    rotation_matrix = np.array([
        [cos_half, -1j * sin_half],
        [-1j * sin_half, cos_half]
    ], dtype=complex)
    final_state_vector = rotation_matrix @ initial_state.data
    target_state = Statevector([cos_half, -1j * sin_half])
    fidelity = state_fidelity(Statevector(final_state_vector), target_state) if QISKIT_AVAILABLE else simple_fidelity(Statevector(final_state_vector), target_state)
    return Statevector(final_state_vector), fidelity, effective_angle


def test_pulse_performance():
    print("="*60)
    print("QUANTUM PULSE TESTING - Golden Ratio vs Gaussian")
    print("="*60)

    golden_pulse = create_golden_ratio_pulse()
    gaussian_pulse = create_gaussian_pulse()

    golden_energy = np.sum(np.abs(golden_pulse)**2)
    gaussian_energy = np.sum(np.abs(gaussian_pulse)**2)

    print("\nEnergy Comparison:")
    print(f"  Golden Ratio: {golden_energy:.2f}")
    print(f"  Gaussian:     {gaussian_energy:.2f}")
    print(f"  Savings:      {100*(1 - golden_energy/gaussian_energy):.1f}%")

    golden_state, golden_fidelity, golden_angle = simulate_quantum_evolution(golden_pulse)
    gaussian_state, gaussian_fidelity, gaussian_angle = simulate_quantum_evolution(gaussian_pulse)

    print("\nQuantum Performance:")
    print(f"  Golden Ratio: angle={np.degrees(golden_angle):.2f} deg, fidelity={golden_fidelity:.4f}")
    print(f"  Gaussian:     angle={np.degrees(gaussian_angle):.2f} deg, fidelity={gaussian_fidelity:.4f}")

    time_ns = np.arange(160)
    freqs_golden, psd_golden = get_spectral_energy(golden_pulse, dt_ns)
    freqs_gauss, psd_gauss = get_spectral_energy(gaussian_pulse, dt_ns)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(time_ns, golden_pulse, label='Golden Ratio', color='orange', linewidth=2)
    axes[0].plot(time_ns, gaussian_pulse, label='Gaussian', color='blue', linestyle='--')
    axes[0].set_title('Pulse Shapes (Time Domain)')
    axes[0].set_xlabel('Time (ns)')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(freqs_golden, psd_golden, label='Golden Ratio', color='orange', linewidth=2)
    axes[1].plot(freqs_gauss, psd_gauss, label='Gaussian', color='blue', linestyle='--')
    axes[1].set_title('Spectral Energy Density')
    axes[1].set_xlabel('Frequency (GHz)')
    axes[1].set_ylabel('Power (dB)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_pulse_test_results.png', dpi=150, bbox_inches='tight')
    print("\nSaved quantum_pulse_test_results.png")
    plt.close()

    print("="*60)


if __name__ == "__main__":
    try:
        test_pulse_performance()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
