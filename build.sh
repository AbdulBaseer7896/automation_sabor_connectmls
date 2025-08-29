#!/bin/bash
echo "Starting build process..."

# Set the correct paths for Chromium and ChromeDriver
export CHROMIUM_PATH=$(which chromium-browser)
export CHROMEDRIVER_PATH=$(which chromedriver)

echo "Chromium path: $CHROMIUM_PATH"
echo "ChromeDriver path: $CHROMEDRIVER_PATH"

# Make sure chromedriver is executable
if [ -f "$CHROMEDRIVER_PATH" ]; then
    chmod +x $CHROMEDRIVER_PATH
    echo "Made chromedriver executable"
fi

# Install Python dependencies
pip install -r requirements.txt

echo "Build completed successfully"