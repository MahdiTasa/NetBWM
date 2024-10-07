#!/bin/bash

# Update package list and install necessary packages
sudo apt-get update
sudo apt-get install -y python3 python3-venv curl vnstat

# Create a directory for the NetBWM project
mkdir -p /opt/netbwm
cd /opt/netbwm

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install psutil matplotlib

# Download the Python script and save it in the appropriate directory
curl -o netbwm_monitor.py https://raw.githubusercontent.com/MahdiTasa/NetBWM/master/netbwm_monitor.py

# Create a systemd service file for the Python script
cat <<EOF | sudo tee /etc/systemd/system/netbwm.service
[Unit]
Description=NetBWM Network Bandwidth Monitor Service
After=network.target

[Service]
ExecStart=/opt/netbwm/venv/bin/python /opt/netbwm/netbwm_monitor.py
WorkingDirectory=/opt/netbwm
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable netbwm.service
sudo systemctl start netbwm.service

# Clean up the old tsbw script if it exists
if [ -f "/usr/local/bin/tsbw" ]; then
    sudo rm /usr/local/bin/tsbw
fi

# Create a new command for running the Python script manually
cat <<'EOL' | sudo tee /usr/local/bin/tsbw
#!/bin/bash
source /opt/netbwm/venv/bin/activate
python /opt/netbwm/netbwm_monitor.py $@
EOL

# Make the tsbw command executable
sudo chmod +x /usr/local/bin/tsbw

# Display installation success message
echo "NetBWM setup completed successfully. You can run it using the command: tsbw"