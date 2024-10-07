import os
import subprocess
from datetime import datetime

# Function to parse vnstat output for hourly, daily, and monthly statistics
def parse_vnstat_output(report_type):
    command = f"vnstat {report_type}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
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
            if len(parts) >= 4:
                data.append({
                    'time': parts[0],
                    'rx': parts[1],
                    'tx': parts[3],
                    'total': parts[5],
                    'avg_rate': parts[7]
                })
        except IndexError:
            pass
    return data

# Function to display parsed data
def display_data(data):
    print("\n+---------------------+--------------+--------------+--------------+--------------+")
    print("| Time                | Received (rx)| Transmitted (tx)| Total        | Average Rate |")
    print("+---------------------+--------------+--------------+--------------+--------------+")
    for entry in data:
        print(f"| {entry['time']:<19} | {entry['rx']:<12} | {entry['tx']:<12} | {entry['total']:<12} | {entry['avg_rate']:<12} |")
    print("+---------------------+--------------+--------------+--------------+--------------+")

# Function to calculate overall sum for rx and tx across interfaces
def calculate_totals(report_type):
    command = "vnstat"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    total_rx = 0
    total_tx = 0
    for line in lines:
        if 'rx' in line and 'tx' in line and report_type in line:
            parts = line.split()
            try:
                rx_value = float(parts[2])
                tx_value = float(parts[5])
                total_rx += rx_value
                total_tx += tx_value
            except ValueError:
                pass

    return total_rx, total_tx

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
    print(f"Total Received: {total_rx} GiB")
    print(f"Total Transmitted: {total_tx} GiB")

if __name__ == "__main__":
    main()