#!/bin/bash

# Update package list and install vnstat
sudo apt-get update
sudo apt-get install -y vnstat bc

# Copy the tsbw script to /usr/local/bin
if [ -f "tsbw" ]; then
    sudo cp tsbw /usr/local/bin/tsbw
    sudo chmod +x /usr/local/bin/tsbw
    echo "NetBWM setup completed successfully. You can run it using the command: tsbw"
else
    echo "Error: tsbw script not found in the current directory. Make sure the script is in the same directory as setup.sh."
    exit 1
fi
