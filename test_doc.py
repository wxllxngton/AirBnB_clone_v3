#!/usr/bin/python3
"""Testing documentation of a module
"""
from importlib import import_module
import sys
import os

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2:
    print("Usage: python script.py <module_name>")
    sys.exit(1)

module_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
module_path = os.path.dirname(os.path.abspath(sys.argv[1]))

# Add the module's directory to the Python path
sys.path.append(module_path)

# Use the module name in your script
m_imported = import_module(module_name)

if m_imported.__doc__ is None:
    print("No module documentation")
else:
    print("OK")

