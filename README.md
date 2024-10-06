# NetBWM (🌐📊 Monitor & Limiter)

NetBWM is a simple 🖥️ script that 📡 monitors 🌐 bandwidth usage and calculates 📈 average rates using `vnstat`. It provides users with an easy way to get real-time 📊 on 🌐 usage, including 🕒 hourly, 📅 daily, and 📆 monthly reports.

## Features
- Monitor 🕒 hourly, 📅 daily, or 📆 monthly 🌐 usage.
- Display 🌐 usage intelligently in appropriate units (Kbit/s, Mbit/s, Gbit/s).
- Easy to use with a simple command: `tsbw`.

## 🛠️ Installation
To install NetBWM, run the following commands:

```bash
git clone https://github.com/mahditasa/NetBWM.git
cd NetBWM
echo '#!/bin/bash

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
fi' > setup.sh
chmod +x setup.sh
sudo ./setup.sh
```

This will install `vnstat` (if not already installed), and copy the script `tsbw` to `/usr/local/bin` so that it can be easily accessed.

## ▶️ Usage
Run the following command to monitor 🌐 usage based on your selected period:

```bash
tsbw
```

After running the command, you will be prompted to choose one of the following options:
- **🕒 Hourly (-h)**: Displays average receive rate for the current hour.
- **📅 Daily (-d)**: Displays average receive rate for today.
- **📆 Monthly (-m)**: Displays average receive rate for the current month.

The result will be shown in the most appropriate unit (e.g., Mbit/s, Gbit/s).

## 🔧 Setup Script (`setup.sh`)
The `setup.sh` script automates the installation of necessary dependencies (`vnstat` and `bc`), copies the `tsbw` script to `/usr/local/bin`, and makes it executable. This ensures that you can easily run the tool using the command `tsbw`.

### How to Run Setup Script
1. Clone the repository:
   ```bash
   git clone https://github.com/mahditasa/NetBWM.git
   ```
2. Navigate to the project directory:
   ```bash
   cd NetBWM
   ```
3. Run the setup script:
   ```bash
   sudo ./setup.sh
   ```

The setup script will:
- Update the package list.
- Install `vnstat` and `bc` (if not already installed).
- Copy the `tsbw` script to `/usr/local/bin` for global access.

After running the setup, you can monitor network bandwidth by simply using the `tsbw` command.

## 📜 License
This project is licensed under the MIT License.
