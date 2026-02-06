"""
Unit tests for quantum pulse comparison.
Aligns with snapshot: Phi, Gaussian, DRAG, Square, Sinc, Raised Cosine, Gaussian Square.
Run with: python test_pulses_unit.py or run_test.bat
"""
import sys
import numpy as np

from pulse_comparison import (
    create_golden_ratio_pulse,
    create_gaussian_pulse,
    create_drag_pulse,
    create_square_pulse,
    create_sinc_pulse,
    create_raised_cosine_pulse,
    create_gaussian_square_pulse,
    get_spectral_energy,
    SAMPLE_RATE_GS,
)

# Expected energies (duration=160) - from snapshot / pulse_comparison
EXPECTED_ENERGIES = {
    'Phi (Golden Ratio)': 36.95,
    'Gaussian': 56.36,
    'DRAG': 56.35,
    'Square': 160.0,
    'Sinc': 19.41,
    'Raised Cosine': 59.64,
    'Gaussian Square': 80.16,
}


def test_all_pulses_normalized():
    """All pulses should have max amplitude 1.0."""
    duration = 160
    pulses = [
        create_golden_ratio_pulse(duration),
        create_gaussian_pulse(duration),
        create_drag_pulse(duration),
        create_square_pulse(duration),
        create_sinc_pulse(duration),
        create_raised_cosine_pulse(duration),
        create_gaussian_square_pulse(duration),
    ]
    for p in pulses:
        assert np.max(np.abs(p)) <= 1.0 + 1e-10, f"Pulse not normalized: max={np.max(np.abs(p))}"
        assert len(p) == duration


def test_spectral_energy_returns_ghz():
    """Frequency axis should be in GHz."""
    duration = 160
    samples = create_gaussian_pulse(duration)
    freqs, psd = get_spectral_energy(samples)
    assert np.max(np.abs(freqs)) <= 0.6
    assert len(freqs) == duration
    assert len(psd) == duration


def test_golden_ratio_less_energy_than_gaussian():
    """Golden Ratio should use less energy than Gaussian."""
    duration = 160
    golden = create_golden_ratio_pulse(duration)
    gauss = create_gaussian_pulse(duration)
    e_golden = np.sum(np.abs(golden)**2)
    e_gauss = np.sum(np.abs(gauss)**2)
    assert e_golden < e_gauss


def test_energies_match_snapshot():
    """Pulse energies must match snapshot / pulse_comparison results."""
    duration = 160
    pulses = {
        'Phi (Golden Ratio)': create_golden_ratio_pulse(duration),
        'Gaussian': create_gaussian_pulse(duration),
        'DRAG': create_drag_pulse(duration),
        'Square': create_square_pulse(duration),
        'Sinc': create_sinc_pulse(duration),
        'Raised Cosine': create_raised_cosine_pulse(duration),
        'Gaussian Square': create_gaussian_square_pulse(duration),
    }
    for name, p in pulses.items():
        e = np.sum(np.abs(p)**2)
        expected = EXPECTED_ENERGIES[name]
        assert abs(e - expected) < 0.1, f"{name}: got {e:.2f}, expected ~{expected}"


if __name__ == "__main__":
    tests = [test_all_pulses_normalized, test_spectral_energy_returns_ghz,
             test_golden_ratio_less_energy_than_gaussian, test_energies_match_snapshot]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failed += 1
    print(f"\n{failed} failed, {len(tests) - failed} passed")
    try:
        input("\nPress Enter to close...")
    except EOFError:
        pass
    sys.exit(failed)
