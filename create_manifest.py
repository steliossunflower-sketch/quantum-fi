"""
Generate reproducibility manifest (Python version, package versions, command).
Run: python create_manifest.py
Output: reproduce_manifest.json and reproduce_manifest.txt
"""
import json
import sys
import subprocess
from datetime import datetime


def main():
    manifest = {
        "generated": datetime.now().isoformat(),
        "python_version": sys.version,
        "commands": {
            "pulse_comparison": "python pulse_comparison.py",
            "export_report": "python export_report.py",
            "unit_tests": "python test_pulses_unit.py",
            "quantum_tests": "python test_pulse_quantum.py",
        },
    }

    try:
        out = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        manifest["packages"] = [l.strip() for l in out.stdout.splitlines() if "==" in l]
    except Exception as e:
        manifest["packages"] = [f"Error: {e}"]

    with open("reproduce_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("Saved reproduce_manifest.json")

    txt = f"""Phi Pulse Reproducibility Manifest
Generated: {manifest['generated']}
Python: {manifest['python_version']}

Commands:
  pulse_comparison: {manifest['commands']['pulse_comparison']}
  export_report:   {manifest['commands']['export_report']}
  unit_tests:      {manifest['commands']['unit_tests']}

Packages ({len(manifest['packages'])}):
"""
    for p in manifest["packages"][:20]:
        txt += f"  {p}\n"
    if len(manifest["packages"]) > 20:
        txt += f"  ... and {len(manifest['packages']) - 20} more\n"

    with open("reproduce_manifest.txt", "w") as f:
        f.write(txt)
    print("Saved reproduce_manifest.txt")
    return manifest


if __name__ == "__main__":
    main()
