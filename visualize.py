#!/usr/bin/env python3
"""
Copyright (C) 2025 Thomas LE Guillou

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.widgets import MultiCursor
from matplotlib.ticker import ScalarFormatter
import matplotlib.dates as md
import numpy as np
import argparse
import json
import os



# Extract the CSV file path
parser = argparse.ArgumentParser(description='Display solisart data')
parser.add_argument('--csv', '-c', help='csv file to parse')
parser.add_argument('--day', '-d', help='day of the month to display')

# Set default config path
script_dir = os.path.dirname(os.path.abspath(__file__))
default_config_path = os.path.join(script_dir, "figure_config.json")
parser.add_argument('--config', '-f', default=default_config_path, help=f'figure configuration JSON file (default: {default_config_path})')
args = parser.parse_args()



# Load figure configuration
def load_figure_config(config_path):
    """Load figure configuration from JSON file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {config_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        exit(1)

# Load the figure structure from JSON
figure_struct = load_figure_config(args.config)

# Clean the CSV file
out = ""
headerAlreadyFound = False
with open(args.csv, "r+") as fd:
    for line in fd.read().splitlines():
        if "Solis" not in line:
            if "Date" in line:
                if not headerAlreadyFound:
                    out = out + f"{line}\r\n"
                    headerAlreadyFound = True
            elif line.split("/")[0] == str(args.day):
                    out = out + f"{line}\r\n"

args.csv = args.csv.replace(".csv", ".clean.csv")
with open(args.csv, "w+") as fd:
    fd.write(out)

# Read the CSV file
data = pd.read_csv(args.csv, delimiter=";")

# Extract the required columns
date_column = pd.to_datetime(data["Date"], format="%d/%m/%y %H:%M")
fig, ax = plt.subplots(len(figure_struct), 1, figsize=(10, 10), sharex=True)

# Set the window title to the CSV filename with day number
csv_filename = os.path.basename(args.csv.replace(".clean.csv", ".csv"))  # Get just the filename
window_title = f"{csv_filename} - day {args.day}"
fig.canvas.manager.set_window_title(window_title)  # Set the actual window title

# Plot figures
plotId = 0
for subp in figure_struct:
    for k, v in subp["data"].items():
        ax[plotId].plot(date_column, data[k], label=v)
    ax[plotId].set_title(subp["name"])
    ax[plotId].set_ylabel(subp["y_label"])
    
    # Move legend outside for plots with many series
    if len(subp["data"]) > 4:  # If more than 4 data series
        ax[plotId].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        ax[plotId].legend()
    
    xfmt = md.DateFormatter("%d/%m@%H:%M:%S")
    ax[plotId].xaxis.set_major_formatter(xfmt)
    
    # Fix X-axis label crowding
    ax[plotId].tick_params(axis='x', labelsize=8, rotation=45)  # Smaller font and rotate labels
    ax[plotId].xaxis.set_tick_params(pad=5)  # Add padding for X-axis labels
    
    # Reduce number of X-axis ticks to prevent crowding
    ax[plotId].xaxis.set_major_locator(plt.MaxNLocator(8))  # Max 8 ticks on X-axis
    
    # Set Y-axis limits if specified in config
    if "y_limit" in subp:
        ax[plotId].set_ylim([subp["y_limit"]["min"], subp["y_limit"]["max"]])
    
    # Fix Y-axis label crowding
    ax[plotId].tick_params(axis='y', labelsize=9)  # Smaller font size for Y-axis labels
    ax[plotId].yaxis.set_tick_params(pad=8)  # Add more padding between axis and labels
    
    # Reduce number of Y-axis ticks to prevent crowding
    ax[plotId].yaxis.set_major_locator(plt.MaxNLocator(6))  # Max 6 ticks on Y-axis
    
    # Enable proper Y-axis formatting
    ax[plotId].yaxis.set_major_formatter(ScalarFormatter())
    
    plotId = plotId + 1

multi = MultiCursor(None, ax, color="black", lw=1)
plt.tight_layout()
plt.subplots_adjust(left=0.12, bottom=0.15)  # Give more space for both Y and X axis labels
plt.show() 