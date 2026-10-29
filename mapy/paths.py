"""
Repository paths, resolved from this file so scripts and notebooks run from any directory.
"""
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')  ## Inputs and caches, not tracked by git
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')  ## Generated figures and tables
