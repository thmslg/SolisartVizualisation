# Solisart Data Visualization Tool

A Python script for visualizing and analyzing data from Solisart solar heating systems. This tool processes CSV data files and generates comprehensive charts showing temperature readings, circulator status, and boiler information.

## Disclaimer

**Important Notice**: This tool is an independent, open-source project created for personal use and educational purposes. I am NOT affiliated with, endorsed by, or related to the Solisart company or its products in any way. This software is provided "as is" without any warranties or guarantees. Use at your own risk and discretion.

## Features

- **Multi-panel visualization** with 4 different chart types:
  - Temperature Zone de vie (Living areas temperature)
  - Temperature installation (Installation temperature)
  - Circulateurs (Circulators status)
  - Chaudiere (Boiler information)
- **Interactive plotting** with matplotlib MultiCursor for synchronized crosshairs
- **Data filtering** by specific day of the month
- **Automatic data cleaning** to remove invalid entries

## Requirements

- Docker

## Installation

1. Clone or download this repository
2. Make the script executable:
```bash
chmod +x run_visualization.sh
```

## Usage

#### Setup X11 forwarding (run once per session)
```bash
xhost +local:docker
```

#### Run with the shell script (recommended)
```bash
./run_visualization.sh <csv_file_path> <day_of_month>
```

**Example:**
```bash
./run_visualization.sh ./example/donnees-SC2M202XXXX-2025-07.csv 22
```

This will:
1. Clean the CSV file by filtering data for the specified day of each month
2. Create a cleaned version with `.clean.csv` suffix
3. Generate an interactive plot with 4 subplots showing different system metrics

![example](./example/SC2M202XXXXX-2025-07-22.png)

[!NOTE]
You have to download manually your csv data as per illustrated here:
![download csv](./HowToDownloadCSVFromSolisart.png)

### Parameters

- `csv_file_path`: Path to the CSV data file to process
- `day_of_month`: Day of the month to display (1-31)

### Advanced Usage

For advanced users who prefer direct Docker commands, see the detailed Docker command in the `run_visualization.sh` script.

#### Customizing Subplot Configuration

The visualization tool uses a JSON configuration file (`figure_config.json`) to define the structure and appearance of each subplot. You can customize this file to modify which data columns are displayed, their labels, and plot settings.

**Configuration File Structure:**

The `figure_config.json` file contains an array of subplot objects, where each object defines one subplot with the following properties:

- **`name`** (string): The title displayed above the subplot
- **`data`** (object): A key-value mapping where:
  - **Key**: CSV column name (e.g., "TZ1", "Text", "HC/HP")
  - **Value**: Display label for the legend (e.g., "1er (mesure)", "Extérieur")
- **`y_label`** (string): Y-axis label with units (e.g., "[°C]", "[%]")
- **`y_limit`** (optional object): Y-axis limits with:
  - **`min`** (number): Minimum Y-axis value
  - **`max`** (number): Maximum Y-axis value

**Example Configuration:**
```json
[
    {
        "name": "Température Zone de vie",
        "data": {
            "TZ1": "1er (mesure)",
            "Tcons1": "1er (consigne)",
            "TZ2": "RDC (mesure)",
            "Tcons2": "RDC (consigne)"
        },
        "y_label": "[°C]",
        "y_limit": {
            "min": 20,
            "max": 30
        }
    }
]
```

**Customization Options:**

1. **Add/Remove Data Series**: Modify the `data` object to include or exclude specific CSV columns
2. **Change Labels**: Update the display names in the `data` values to customize legend labels
3. **Set Y-Axis Limits**: Add a `y_limit` object to control the Y-axis range for better visualization
4. **Modify Units**: Change the `y_label` to reflect different measurement units
5. **Reorder Subplots**: Rearrange the array order to change subplot positioning

**Using a Custom Configuration:**
```bash
./run_visualization.sh --config my_custom_config.json ./example/data.csv 22
```

## Data Format

The script expects CSV files with the following columns:
- `Date`: Timestamp in format "DD/MM/YY HH:MM"
- Temperature columns: `TZ1`, `TZ2`, `TZ3`, `Text`, `Tcapt`, etc.
- Circulator columns: `HC/HP`, `APP`, `SOL`, `BTC`, `C1`, `C2`, `C3`
- Boiler columns: `chdr1`

## Output

The script generates an interactive matplotlib window with:
- Synchronized time axis across all subplots
- MultiCursor for precise data point inspection
- Legend for each data series
- Automatic scaling and formatting

## X11 Forwarding Setup (Docker)

For Docker usage, you need to enable X11 forwarding to display matplotlib windows on your host system:

### One-time setup (per session)
```bash
xhost +local:docker
```

## License

This project is licensed under the GNU General Public License v3.0 - see **SPDX-License-Identifier:** GPL-3.0-or-later

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Thomas Le Guillou - 2025