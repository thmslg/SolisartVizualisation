FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies for matplotlib and Tkinter
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY visualize.py .
COPY figure_config.json .

# Set environment variable for matplotlib backend (will be overridden by X11 if available)
ENV MPLBACKEND=TkAgg

# Set the default command
ENTRYPOINT ["python", "visualize.py"] 