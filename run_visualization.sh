#!/bin/bash

# Check if correct number of arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <csv_file_path> <day_of_month>"
    echo "Example: $0 ./example/donnees-SC2M202XXXX-2025-07.csv 22"
    exit 1
fi

CSV_FILE_PATH="$1"
DAY_OF_MONTH="$2"

# Check if CSV file exists
if [ ! -f "$CSV_FILE_PATH" ]; then
    echo "Error: CSV file '$CSV_FILE_PATH' not found!"
    exit 1
fi

# Check if day is a valid number (1-31)
if ! [[ "$DAY_OF_MONTH" =~ ^[1-9]$|^[12][0-9]$|^3[01]$ ]]; then
    echo "Error: Day must be a number between 1 and 31"
    exit 1
fi

# Get the absolute path of the CSV file
CSV_ABSOLUTE_PATH=$(realpath "$CSV_FILE_PATH")
CSV_DIR=$(dirname "$CSV_ABSOLUTE_PATH")
CSV_FILENAME=$(basename "$CSV_ABSOLUTE_PATH")

# Get the current directory (where the Dockerfile is located)
SCRIPT_DIR=$(dirname "$(realpath "$0")")

echo "Running visualization for:"
echo "  CSV file: $CSV_FILE_PATH"
echo "  Day: $DAY_OF_MONTH"
echo ""

# Build the Docker image if it doesn't exist or if Dockerfile is newer
if [ ! "$(docker images -q solisart-visualization 2> /dev/null)" ] || [ "$(docker images -q solisart-visualization 2> /dev/null)" == "" ]; then
    echo "Building Docker image..."
    docker build -t solisart-visualization "$SCRIPT_DIR"
fi

# Run the Docker container
# Mount the CSV file directory and pass the arguments
docker run --rm \
    -e DISPLAY="$DISPLAY" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$CSV_DIR":/data \
    -v "$SCRIPT_DIR":/app \
    solisart-visualization \
    --csv "/data/$CSV_FILENAME" --day "$DAY_OF_MONTH" 