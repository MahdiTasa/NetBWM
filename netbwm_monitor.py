import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt

# Function to parse vnstat output for hourly, daily, and monthly statistics
def parse_vnstat_output(report_type):
    command = ["vnstat", report_type]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Function to extract relevant data from vnstat output
def extract_data(vnstat_output):
    lines = vnstat_output.splitlines()
    data = []
    for line in lines:
        if 'rx' in line and 'tx' in line:
            continue
        try:
            parts = line.split()
            if len(parts) >= 11:
                data.append({
                    'time': parts[0],
                    'rx': parts[1] + ' ' + parts[2],
                    'tx': parts[4] + ' ' + parts[5],
                    'total': parts[7] + ' ' + parts[8],
                    'avg_rate_rx': parts[9] + ' ' + parts[10],
                    'avg_rate_tx': parts[11] + ' ' + parts[12] if len(parts) > 12 else ''
                })
        except IndexError:
            pass
    return data

# Function to display parsed data
def display_data(data):
    print("\n+---------------------+--------------+--------------+--------------+--------------+--------------+")
    print("| Time                | Received (rx)| Transmitted (tx)| Total        | Avg Rate RX  | Avg Rate TX  |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")
    for entry in data:
        print(f"| {entry['time']:<19} | {entry['rx']:<12} | {entry['tx']:<12} | {entry['total']:<12} | {entry['avg_rate_rx']:<12} | {entry['avg_rate_tx']:<12} |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")

# Function to calculate overall sum for rx and tx across interfaces
def calculate_totals(report_type):
    command = ["vnstat"]
    result = subprocess.run(command, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    total_rx = 0
    total_tx = 0
    for line in lines:
        if 'rx' in line and 'tx' in line and report_type in line:
            parts = line.split()
            try:
                rx_value = float(parts[1].replace('GiB', '').replace('MiB', '').replace('KiB', ''))
                tx_value = float(parts[4].replace('GiB', '').replace('MiB', '').replace('KiB', ''))
                if 'GiB' in parts[1]:
                    total_rx += rx_value
                elif 'MiB' in parts[1]:
                    total_rx += rx_value / 1024
                elif 'KiB' in parts[1]:
                    total_rx += rx_value / (1024 * 1024)
                if 'GiB' in parts[4]:
                    total_tx += tx_value
                elif 'MiB' in parts[4]:
                    total_tx += tx_value / 1024
                elif 'KiB' in parts[4]:
                    total_tx += tx_value / (1024 * 1024)
            except ValueError:
                pass

    return total_rx, total_tx

# Function to plot bandwidth usage
def plot_bandwidth(data):
    times = [entry['time'] for entry in data]
    rx_rates = [float(entry['avg_rate_rx'].split()[0]) for entry in data if entry['avg_rate_rx']]

    plt.figure(figsize=(10, 6))
    plt.plot(times, rx_rates, label='Receive Rate (rx)', color='b')
    plt.xlabel('Time')
    plt.ylabel('Bandwidth (Mbit/s)')
    plt.title('Bandwidth Usage (Receive) - 98% Capacity')
    plt.axhline(y=0.98 * max(rx_rates), color='r', linestyle='--', label='98% Capacity')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Main function to provide the menu and options to the user
def main():
    while True:
        print("Choose a report type:")
        print("1) Hourly (-h)")
        print("2) Daily (-d)")
        print("3) Monthly (-m)")
        choice = input("Enter the number (1-3): ")
        
        if choice in ['1', '2', '3']:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

    report_type = '-h' if choice == '1' else ('-d' if choice == '2' else '-m')
    vnstat_output = parse_vnstat_output(report_type)
    data = extract_data(vnstat_output)
    display_data(data)

    total_rx, total_tx = calculate_totals(report_type)
    print("\nTotal Bandwidth Usage Across All Interfaces:")
    print(f"Total Received: {total_rx:.2f} GiB")
    print(f"Total Transmitted: {total_tx:.2f} GiB")

    plot_bandwidth(data)

if __name__ == "__main__":
    main()