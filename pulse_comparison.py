"""
Quantum Pulse Comparison: Phi (Golden Ratio) vs all quantum pulse types.
Compares the Phi pulse with Gaussian, DRAG, Square, Sinc, Raised Cosine, Gaussian Square.
Sample rate: 1 GS/s. Time in ns, Frequency in GHz.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq

SAMPLE_RATE_GS = 1.0
dt_sec = 1e-9  # 1 ns per sample at 1 GS/s


def create_phi_pulse(duration, t_min=-6, t_max=5):
    """Phi pulse: A(t) = phi^(-t(t+1)/2)"""
    PHI = (1 + np.sqrt(5)) / 2
    t_vals = np.linspace(t_min, t_max, duration)
    samples = PHI ** (-(t_vals * (t_vals + 1)) / 2)
    return samples / np.max(np.abs(samples))


def create_golden_ratio_pulse(duration, t_min=-6, t_max=5):
    """Alias for Phi pulse."""
    return create_phi_pulse(duration, t_min, t_max)


def create_gaussian_pulse(duration):
    """Standard Gaussian envelope."""
    sigma = duration / 5
    t = np.linspace(-duration/2, duration/2, duration)
    samples = np.exp(-(t**2) / (2 * sigma**2))
    return samples / np.max(np.abs(samples))


def create_drag_pulse(duration, beta=0.1):
    """DRAG: Derivative Removal by Adiabatic Gate."""
    sigma = duration / 5
    t = np.linspace(-duration/2, duration/2, duration)
    gauss = np.exp(-(t**2) / (2 * sigma**2))
    derivative = -t / (sigma**2) * gauss
    samples = gauss + beta * derivative
    return samples / np.max(np.abs(samples))


def create_square_pulse(duration):
    """Rectangular/constant envelope."""
    return np.ones(duration)


def create_sinc_pulse(duration):
    """Sinc pulse: band-limited."""
    t = np.linspace(-4, 4, duration)
    samples = np.sinc(t)
    return samples / np.max(np.abs(samples))


def create_raised_cosine_pulse(duration):
    """Raised cosine: smooth, zero at edges."""
    t = np.linspace(-1, 1, duration)
    samples = 0.5 * (1 + np.cos(np.pi * t))
    samples = np.maximum(samples, 0)
    return samples / np.max(np.abs(samples))


def create_gaussian_square_pulse(duration, flat_fraction=0.5):
    """Gaussian Square: flat top with Gaussian rise/fall."""
    sigma = duration / 8
    t = np.linspace(-duration/2, duration/2, duration)
    flat_samples = int(duration * (1 - flat_fraction) / 2)
    rise = np.exp(-(t[:flat_samples]**2) / (2 * sigma**2))
    fall = np.exp(-(t[-flat_samples:]**2) / (2 * sigma**2))
    flat = np.ones(duration - 2 * flat_samples)
    samples = np.concatenate([rise, flat, fall])
    return samples / np.max(np.abs(samples))


def compute_leakage_metrics(samples, dt=1e-9, high_freq_threshold_frac=0.2):
    """Compute leakage % and bandwidth at -40dB. Returns (leakage_pct, bandwidth_GHz)."""
    freqs, psd = get_spectral_energy(samples, dt)
    nyquist = 0.5 * SAMPLE_RATE_GS
    threshold = high_freq_threshold_frac * nyquist
    mask = np.abs(freqs) > threshold
    psd_linear = 10 ** (psd / 10)
    total = np.sum(psd_linear)
    leakage = np.sum(psd_linear[mask]) / total * 100 if total > 0 else 0
    cutoff_db = -40
    cutoff_idx = np.where(psd < cutoff_db)[0]
    bandwidth = 2 * np.max(np.abs(freqs[cutoff_idx])) if len(cutoff_idx) > 0 else nyquist * 2
    return leakage, bandwidth


def get_spectral_energy(samples, dt=1e-9):
    """Compute PSD. Returns (freq_GHz, psd_dB)."""
    n = len(samples)
    yf = fft(samples)
    xf_Hz = fftfreq(n, dt)
    yf_shifted = fftshift(yf)
    xf_shifted = fftshift(xf_Hz)
    xf_GHz = xf_shifted / 1e9
    psd = 20 * np.log10(np.abs(yf_shifted) + 1e-15)
    psd = psd - np.max(psd)
    return xf_GHz, psd


def run_pulse_comparison():
    duration = 160
    t_min, t_max = -6, 5

    pulses = {
        'Phi (Golden Ratio)': create_phi_pulse(duration, t_min, t_max),
        'Gaussian': create_gaussian_pulse(duration),
        'DRAG': create_drag_pulse(duration),
        'Square': create_square_pulse(duration),
        'Sinc': create_sinc_pulse(duration),
        'Raised Cosine': create_raised_cosine_pulse(duration),
        'Gaussian Square': create_gaussian_square_pulse(duration),
    }

    spectra = {name: get_spectral_energy(samples, dt_sec) for name, samples in pulses.items()}
    energies = {name: np.sum(np.abs(samples)**2) for name, samples in pulses.items()}

    phi_energy = energies['Phi (Golden Ratio)']
    time_ns = np.arange(duration)
    colors = ['#e65100', '#1565c0', '#2e7d32', '#c62828', '#6a1b9a', '#00838f', '#f9a825']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for idx, (name, samples) in enumerate(pulses.items()):
        ax1.plot(time_ns, samples, label=name, color=colors[idx % len(colors)],
                 linewidth=2, alpha=0.9)

    ax1.set_title('Time Domain: Phi Pulse vs Quantum Pulse Types')
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Amplitude (normalized)')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, duration)

    for idx, (name, (freqs, psd)) in enumerate(spectra.items()):
        ax2.plot(freqs, psd, label=name, color=colors[idx % len(colors)],
                 linewidth=2, alpha=0.9)

    ax2.set_title('Spectral Energy Density (Leakage Check)')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Power Spectral Density (dB)')
    ax2.set_ylim(-100, 5)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Phi Pulse vs All Quantum Pulse Types - Sample Rate 1 GS/s',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('pulse_comparison.png', dpi=150, bbox_inches='tight')
    print("Plot saved as 'pulse_comparison.png'")
    if os.path.isdir('website'):
        plt.savefig(os.path.join('website', 'pulse_comparison.png'), dpi=150, bbox_inches='tight')
        with open(os.path.join('website', 'pulse_data.json'), 'w') as f:
            json.dump(energies, f, indent=2)
        print("Plot and pulse_data.json saved to website/")
    plt.close()

    print("\n" + "="*60)
    print("PULSE COMPARISON - Phi vs All Types")
    print("="*60)
    for name, e in energies.items():
        savings = 100 * (1 - phi_energy / e) if e > 0 else 0
        print(f"  {name:20s}: {e:.2f} energy" + (f"  (Phi saves {savings:.1f}%)" if name != 'Phi (Golden Ratio)' else ""))
    print("="*60)


if __name__ == "__main__":
    run_pulse_comparison()
