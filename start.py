#!/usr/bin/env python3
"""Wrapper to launch Streamlit with correct working directory."""
import os
import sys

# Change to the essay-exam-app directory before Streamlit calls os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from streamlit.web.cli import main
sys.argv = ["streamlit", "run", "main.py", "--server.port", "8501", "--server.headless", "true"]
main()
