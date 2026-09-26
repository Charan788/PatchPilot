"""Offline known-fix check. Not an AI or sandbox integration test."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(folder):
    runner = ["pytest", "-q", "tests"] if "--pytest" in sys.argv else ["unittest", "discover", "-s", "tests", "-v"]
    return subprocess.run([sys.executable, "-B", "-m"] + runner,
                          cwd=folder, capture_output=True, text=True, timeout=30)

def main():
    with tempfile.TemporaryDirectory(prefix="patchpilot-") as temp:
        target = Path(temp)
        shutil.copy(ROOT / "app.py", target / "app.py")
        shutil.copytree(ROOT / "tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__"))
        before = run(target)
        print("BASELINE:\n" + before.stdout + before.stderr)
        if before.returncode != 1 or ("FAILED (failures=5)" not in before.stderr and "5 failed, 1 passed" not in before.stdout):
            raise RuntimeError("Expected exactly five assertion failures")
        app = target / "app.py"
        text = app.read_text(encoding="utf-8-sig")
        if text.count("return price + quantity") != 1:
            raise RuntimeError("Unexpected fixture")
        app.write_text(text.replace("return price + quantity", "return price * quantity"), encoding="utf-8")
        after = run(target)
        print("KNOWN FIX IN TEMP COPY:\n" + after.stdout + after.stderr)
        if after.returncode or ("Ran 6 tests" not in after.stderr and "6 passed" not in after.stdout):
            raise RuntimeError("Repair did not pass all six tests")
        print("Fixture verified. Original stays buggy. Live integrations remain untested.")

if __name__ == "__main__":
    main()


