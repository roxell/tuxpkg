"""
Release automation tool for Python projects
"""

__version__ = "0.1.0"


from pathlib import Path


def get_data_file(f):
    path = Path(__file__).parent / "data" / f
    assert path.exists()
    return path
