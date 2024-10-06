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
chmod +x install.sh
sudo ./install.sh
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

## 📜 License
This project is licensed under the MIT License.
