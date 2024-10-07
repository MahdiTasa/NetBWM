import subprocess
import matplotlib.pyplot as plt
import re

# Function to parse vnstat output for hourly, daily, and monthly statistics
def parse_vnstat_output(report_type):
    command = ["vnstat", report_type]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Function to parse size strings like '9.41 GiB'
def parse_size(size_str):
    match = re.match(r'([0-9.]+)\s*(\w+)', size_str)
    if not match:
        return 0
    value, unit = match.groups()
    value = float(value)
    unit = unit.strip()
    units = {
        'B': 1,
        'KiB': 1024,
        'MiB': 1024 ** 2,
        'GiB': 1024 ** 3,
        'TiB': 1024 ** 4,
    }
    return value * units.get(unit, 1)

# Function to parse rate strings like '44.41 Mbit/s'
def parse_rate(rate_str):
    match = re.match(r'([0-9.]+)\s*(\w+)', rate_str)
    if not match:
        return 0
    value, unit = match.groups()
    value = float(value)
    unit = unit.strip()
    units = {
        'bit/s': 1e-6,
        'kbit/s': 1e-3,
        'Mbit/s': 1,
        'Gbit/s': 1e3,
    }
    return value * units.get(unit, 1)  # Return rate in Mbit/s

# Function to extract relevant data from vnstat output
def extract_data(vnstat_output):
    lines = vnstat_output.splitlines()
    data = []
    current_date = ''
    for line in lines:
        line = line.strip()
        # Skip empty lines and separator lines
        if not line or line.startswith('----') or line.startswith('vnstat'):
            continue
        # Capture the date line
        if re.match(r'\d{4}-\d{2}-\d{2}', line):
            current_date = line
            continue
        # Skip headers
        if line.startswith('hour') or line.startswith('day') or line.startswith('month') or line.startswith('year'):
            continue
        if 'rx' in line and 'tx' in line:
            continue
        if 'estimated' in line:
            continue
        # Parse data lines
        if '|' in line:
            # Replace multiple spaces with single space
            line = re.sub(r'\s+', ' ', line)
            # Split the line by '|'
            parts = line.split('|')
            if len(parts) != 4:
                continue
            left_part = parts[0].strip()
            tx_part = parts[1].strip()
            total_part = parts[2].strip()
            avg_rate_part = parts[3].strip()
            # Extract time and rx
            left_parts = left_part.split()
            if len(left_parts) < 3:
                continue
            time_str = left_parts[0]
            rx_value_str = ' '.join(left_parts[1:])
            # Build full time
            if current_date:
                time = f"{current_date} {time_str}"
            else:
                time = time_str
            # Parse numerical values
            rx_value = parse_size(rx_value_str)
            tx_value = parse_size(tx_part)
            total_value = parse_size(total_part)
            avg_rate_value = parse_rate(avg_rate_part)
            data.append({
                'time': time,
                'rx': rx_value,
                'tx': tx_value,
                'total': total_value,
                'avg_rate': avg_rate_value,  # in Mbit/s
            })
    return data

# Function to display parsed data
def display_data(data):
    print("\n+---------------------+--------------+--------------+--------------+--------------+--------------+")
    print("| Time                | Received (rx)| Transmitted (tx)| Total        | Avg Rate RX  | Avg Rate TX  |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")
    for entry in data:
        rx_str = f"{entry['rx'] / (1024 ** 2):.2f} MiB"
        tx_str = f"{entry['tx'] / (1024 ** 2):.2f} MiB"
        total_str = f"{entry['total'] / (1024 ** 2):.2f} MiB"
        avg_rate_str = f"{entry['avg_rate']:.2f} Mbit/s"
        print(f"| {entry['time']:<19} | {rx_str:<12} | {tx_str:<12} | {total_str:<12} | {avg_rate_str:<12} | {'':<12} |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")

# Function to calculate overall sum for rx and tx across interfaces
def calculate_totals(data):
    total_rx = sum(entry['rx'] for entry in data)
    total_tx = sum(entry['tx'] for entry in data)
    return total_rx, total_tx

# Function to plot bandwidth usage
def plot_bandwidth(data):
    times = [entry['time'] for entry in data]
    rx_rates = [entry['avg_rate'] for entry in data]  # avg_rate is in Mbit/s
    tx_rates = [entry['tx'] * 8 / (3600 * 1e6) for entry in data]  # Convert bytes to Mbit/s assuming 1-hour intervals

    plt.figure(figsize=(12, 6))
    plt.plot(times, rx_rates, label='Avg Receive Rate (Mbit/s)', color='b', marker='o')
    plt.plot(times, tx_rates, label='Avg Transmit Rate (Mbit/s)', color='g', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Bandwidth (Mbit/s)')
    plt.title('Bandwidth Usage')
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
    if not data:
        print("\nError: No data available to display.")
        return

    display_data(data)

    total_rx, total_tx = calculate_totals(data)
    print("\nTotal Bandwidth Usage Across All Interfaces:")
    print(f"Total Received: {total_rx / (1024 ** 3):.2f} GiB")
    print(f"Total Transmitted: {total_tx / (1024 ** 3):.2f} GiB")

    plot_bandwidth(data)

if __name__ == "__main__":
    main()
