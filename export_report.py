"""
Export full comparison report (HTML + embedded images).
Run: python export_report.py
Output: report_YYYYMMDD_HHMMSS.html
"""
import os
import base64
from datetime import datetime
from io import BytesIO

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pulse_comparison import (
    create_phi_pulse,
    create_gaussian_pulse,
    create_drag_pulse,
    create_square_pulse,
    create_sinc_pulse,
    create_raised_cosine_pulse,
    create_gaussian_square_pulse,
    get_spectral_energy,
    compute_leakage_metrics,
    SAMPLE_RATE_GS,
    dt_sec,
)


def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def export_html_report(return_content=False):
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

    spectra = {n: get_spectral_energy(s, dt_sec) for n, s in pulses.items()}
    energies = {n: np.sum(np.abs(s)**2) for n, s in pulses.items()}
    leakages = {n: compute_leakage_metrics(s, dt_sec) for n, s in pulses.items()}

    phi_energy = energies['Phi (Golden Ratio)']
    time_ns = np.arange(duration)
    colors = ['#e65100', '#1565c0', '#2e7d32', '#c62828', '#6a1b9a', '#00838f', '#f9a825']

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    for i, (n, s) in enumerate(pulses.items()):
        ax1.plot(time_ns, s, label=n, color=colors[i % len(colors)], linewidth=2)
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Time Domain')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    img1 = fig_to_base64(fig1)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    for i, (n, (freqs, psd)) in enumerate(spectra.items()):
        ax2.plot(freqs, psd, label=n, color=colors[i % len(colors)], linewidth=2)
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('PSD (dB)')
    ax2.set_ylim(-100, 5)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    img2 = fig_to_base64(fig2)
    plt.close(fig2)

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fname = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    rows = []
    for n in pulses:
        e = energies[n]
        lk, bw = leakages[n]
        sav = f"{100*(1 - phi_energy/e):.1f}%" if n != 'Phi (Golden Ratio)' and e > phi_energy else '-'
        rows.append(f"<tr><td>{n}</td><td>{e:.2f}</td><td>{lk:.4f}%</td><td>{bw:.4f}</td><td>{sav}</td></tr>")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Phi Pulse Comparison Report</title>
<style>
body{{ font-family: sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
h1{{ color: #333; }}
table{{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
th,td{{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th{{ background: #f0f0f0; }}
img{{ max-width: 100%; height: auto; margin: 1rem 0; }}
.meta{{ color: #666; font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>Phi Pulse vs Quantum Pulse Types - Report</h1>
<p class="meta">Generated: {ts} | Sample rate: {SAMPLE_RATE_GS} GS/s | Duration: {duration} samples</p>

<h2>Time Domain</h2>
<img src="data:image/png;base64,{img1}" alt="Time domain" style="max-width: 800px;">

<h2>Frequency Domain</h2>
<img src="data:image/png;base64,{img2}" alt="Frequency domain" style="max-width: 800px;">

<h2>Energy & Leakage Metrics</h2>
<table>
<tr><th>Pulse</th><th>Energy</th><th>High-freq Leakage %</th><th>Bandwidth (-40dB) GHz</th><th>Phi Savings</th></tr>
{chr(10).join(rows)}
</table>

<h2>Methodology</h2>
<p>Phi pulse: A(t) = phi^(-t(t+1)/2). Sample rate 1 GS/s. FFT with dt=1e-9 s. Energy = sum(|A|^2).</p>
<p>Reproducible: run python pulse_comparison.py</p>
</body>
</html>"""

    if not return_content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Report saved: {fname}")
        return fname
    return fname, html


if __name__ == "__main__":
    export_html_report()
