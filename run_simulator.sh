#!/bin/bash
# Launcher script for the Voxel Gun Disassembly/Assembly Simulator

# Check if required packages are installed
if ! python3 -c "import pygame" &> /dev/null; then
    echo "Error: Pygame is not installed."
    echo "Please install dependencies with: pip install -r requirements.txt"
    exit 1
fi

if ! python3 -c "import numpy" &> /dev/null; then
    echo "Error: NumPy is not installed."
    echo "Please install dependencies with: pip install -r requirements.txt"
    exit 1
fi

# Run the simulator
echo "Starting Voxel Gun Disassembly/Assembly Simulator..."
echo "Controls will be displayed in the application window."
python3 voxel_gun_simulator.py