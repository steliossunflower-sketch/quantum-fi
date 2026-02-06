"""
Export Phi and other pulses as Qiskit Waveform (.npz) for use with real quantum hardware.
Run: python export_qiskit_waveform.py
Output: phi_pulses.npz (numpy arrays) and optional Qiskit Waveform if qiskit available.
"""
import os
import numpy as np

from pulse_comparison import (
    create_phi_pulse,
    create_gaussian_pulse,
    create_drag_pulse,
    create_square_pulse,
    create_sinc_pulse,
    create_raised_cosine_pulse,
    create_gaussian_square_pulse,
    SAMPLE_RATE_GS,
)


def export_pulses_npz(return_bytes=False):
    duration = 160
    t_min, t_max = -6, 5

    pulses = {
        'phi': create_phi_pulse(duration, t_min, t_max),
        'gaussian': create_gaussian_pulse(duration),
        'drag': create_drag_pulse(duration),
        'square': create_square_pulse(duration),
        'sinc': create_sinc_pulse(duration),
        'raised_cosine': create_raised_cosine_pulse(duration),
        'gaussian_square': create_gaussian_square_pulse(duration),
    }

    dt = 1.0 / (SAMPLE_RATE_GS * 1e9)  # seconds per sample
    buf = {}
    for k, v in pulses.items():
        buf[k] = v
    buf["duration"] = duration
    buf["dt"] = dt
    buf["sample_rate_gs"] = SAMPLE_RATE_GS

    if return_bytes:
        import io
        bio = io.BytesIO()
        np.savez(bio, **pulses, duration=np.array(duration), dt=np.array(dt), sample_rate_gs=np.array(SAMPLE_RATE_GS))
        bio.seek(0)
        return bio.getvalue()

    np.savez('phi_pulses.npz', **pulses, duration=duration, dt=dt, sample_rate_gs=SAMPLE_RATE_GS)
    print("Saved phi_pulses.npz with all pulse arrays (duration, dt, sample_rate_gs).")
    try:
        from qiskit.pulse.library import Waveform
        for name, samples in pulses.items():
            wf = Waveform(samples.astype(complex))
            np.savez(f"waveform_{name}.npz", samples=wf.samples, duration=duration)
            print(f"  Qiskit Waveform '{name}' -> waveform_{name}.npz")
    except ImportError:
        pass
    return 'phi_pulses.npz'


if __name__ == "__main__":
    export_pulses_npz()
