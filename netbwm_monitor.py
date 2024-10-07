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
        line = line.strip()
        # Skip the table header and separator lines
        if line.startswith('+') or line.startswith('| Time') or line.startswith('| ---'):
            continue
        if not line.startswith('|'):
            continue
        # Split the line by '|' and strip whitespace from each part
        parts = line.strip('|').split('|')
        parts = [part.strip() for part in parts]
        if len(parts) >= 6:
            data.append({
                'time': parts[0],
                'rx': parts[1],
                'tx': parts[2],
                'total': parts[3],
                'avg_rate_rx': parts[4],
                'avg_rate_tx': parts[5]
            })
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
    command = ["vnstat", report_type]
    result = subprocess.run(command, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    total_rx = 0
    total_tx = 0
    for line in lines:
        if 'rx' in line and 'tx' in line and not line.startswith(' '):
            parts = line.split()
            try:
                rx_value = float(parts[1])
                rx_unit = parts[2]
                tx_value = float(parts[4])
                tx_unit = parts[5]

                if rx_unit == 'GiB':
                    total_rx += rx_value
                elif rx_unit == 'MiB':
                    total_rx += rx_value / 1024
                elif rx_unit == 'KiB':
                    total_rx += rx_value / (1024 * 1024)

                if tx_unit == 'GiB':
                    total_tx += tx_value
                elif tx_unit == 'MiB':
                    total_tx += tx_value / 1024
                elif tx_unit == 'KiB':
                    total_tx += tx_value / (1024 * 1024)
            except (ValueError, IndexError):
                pass

    return total_rx, total_tx

# Function to plot bandwidth usage
def plot_bandwidth(data):
    times = [entry['time'] for entry in data]
    
    # Convert average rates to float and handle units
    rx_rates = []
    tx_rates = []
    for entry in data:
        # Process average receive rate
        avg_rx = entry['avg_rate_rx']
        if avg_rx:
            rx_value, rx_unit = avg_rx.split()
            rx_value = float(rx_value)
            if rx_unit == 'kbit/s':
                rx_value /= 1000  # Convert to Mbit/s
            elif rx_unit == 'Gbit/s':
                rx_value *= 1000  # Convert to Mbit/s
            rx_rates.append(rx_value)
        else:
            rx_rates.append(0)

        # Process average transmit rate
        avg_tx = entry['avg_rate_tx']
        if avg_tx:
            tx_value, tx_unit = avg_tx.split()
            tx_value = float(tx_value)
            if tx_unit == 'kbit/s':
                tx_value /= 1000  # Convert to Mbit/s
            elif tx_unit == 'Gbit/s':
                tx_value *= 1000  # Convert to Mbit/s
            tx_rates.append(tx_value)
        else:
            tx_rates.append(0)

    # Ensure times, rx_rates, and tx_rates have matching length
    if not times or not rx_rates or len(times) != len(rx_rates):
        print("\nError: Insufficient data for plotting bandwidth usage.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(times, rx_rates, label='Receive Rate (Mbit/s)', color='b', marker='o')
    plt.plot(times, tx_rates, label='Transmit Rate (Mbit/s)', color='g', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Bandwidth (Mbit/s)')
    plt.title('Bandwidth Usage (Receive and Transmit)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
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
