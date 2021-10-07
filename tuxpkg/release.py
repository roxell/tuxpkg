from pathlib import Path
import subprocess
import sys


def run():
    script = Path(__file__).parent / "data" / "release"
    try:
        subprocess.check_call([script])
    except subprocess.CalledProcessError as err:
        sys,exit(err.returncode)
