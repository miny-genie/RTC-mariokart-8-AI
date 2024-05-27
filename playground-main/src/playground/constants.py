import sys
from pathlib import Path

# The base directory where all source files exist.
BASE_DIR = Path(__file__).resolve().parent

# Is this program executed as an exe.
IS_EXE = False

# Setup static files to work with onefile exe.
if hasattr(sys, "_MEIPASS"):
    # https://stackoverflow.com/questions/22472124
    BASE_DIR = BASE_DIR / getattr(sys, "_MEIPASS")
    
    # Is this program executed as an exe.
    IS_EXE = True