import subprocess
import json
import matplotlib.pyplot as plt

# Function to parse vnstat output in JSON format
def parse_vnstat_json(report_type):
    command = ["env", "LANG=C", "vnstat", report_type, "--json"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running vnstat:", result.stderr)
        return None
    data = json.loads(result.stdout)
    return data

# Function to extract relevant data from vnstat JSON output
def extract_data(data, report_type):
    result = []
    interface = data['interfaces'][0]  # Assuming only one interface
    traffic = interface['traffic']

    if report_type == '-h':
        hours = traffic['hours']
        for hour in hours:
            time = '{:02d}:00'.format(hour['hour'])
            rx = hour['rx']
            tx = hour['tx']
            total = rx + tx
            result.append({
                'time': time,
                'rx': rx,
                'tx': tx,
                'total': total,
                'avg_rate_rx': rx / 3600 * 8 / 1e6,  # Convert bytes to Mbit/s
                'avg_rate_tx': tx / 3600 * 8 / 1e6,
            })
    elif report_type == '-d':
        days = traffic['days']
        for day in days:
            date = day['date']
            time = '{year}-{month:02d}-{day:02d}'.format(**date)
            rx = day['rx']
            tx = day['tx']
            total = rx + tx
            result.append({
                'time': time,
                'rx': rx,
                'tx': tx,
                'total': total,
                'avg_rate_rx': rx / (24 * 3600) * 8 / 1e6,  # Mbit/s
                'avg_rate_tx': tx / (24 * 3600) * 8 / 1e6,
            })
    elif report_type == '-m':
        months = traffic['months']
        for month in months:
            date = month['date']
            time = '{year}-{month:02d}'.format(**date)
            rx = month['rx']
            tx = month['tx']
            total = rx + tx
            days_in_month = month['days']
            result.append({
                'time': time,
                'rx': rx,
                'tx': tx,
                'total': total,
                'avg_rate_rx': rx / (days_in_month * 24 * 3600) * 8 / 1e6,  # Mbit/s
                'avg_rate_tx': tx / (days_in_month * 24 * 3600) * 8 / 1e6,
            })
    return result

# Function to display parsed data
def display_data(data):
    print("\n+---------------------+--------------+--------------+--------------+--------------+--------------+")
    print("| Time                | Received (rx)| Transmitted (tx)| Total        | Avg Rate RX  | Avg Rate TX  |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")
    for entry in data:
        rx_str = '{:.2f} MiB'.format(entry['rx'] / (1024*1024))
        tx_str = '{:.2f} MiB'.format(entry['tx'] / (1024*1024))
        total_str = '{:.2f} MiB'.format(entry['total'] / (1024*1024))
        avg_rate_rx_str = '{:.2f} Mbit/s'.format(entry['avg_rate_rx'])
        avg_rate_tx_str = '{:.2f} Mbit/s'.format(entry['avg_rate_tx'])
        print(f"| {entry['time']:<19} | {rx_str:<12} | {tx_str:<12} | {total_str:<12} | {avg_rate_rx_str:<12} | {avg_rate_tx_str:<12} |")
    print("+---------------------+--------------+--------------+--------------+--------------+--------------+")

# Function to plot bandwidth usage
def plot_bandwidth(data):
    times = [entry['time'] for entry in data]
    rx_rates = [entry['avg_rate_rx'] for entry in data]
    tx_rates = [entry['avg_rate_tx'] for entry in data]

    plt.figure(figsize=(12,6))
    plt.plot(times, rx_rates, label='Receive Rate (Mbit/s)', marker='o')
    plt.plot(times, tx_rates, label='Transmit Rate (Mbit/s)', marker='o')
    plt.xlabel('Time')
    plt.ylabel('Bandwidth (Mbit/s)')
    plt.title('Bandwidth Usage')
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
    vnstat_data = parse_vnstat_json(report_type)
    if not vnstat_data:
        print("Error: Could not retrieve vnstat data.")
        return

    data = extract_data(vnstat_data, report_type)
    if not data:
        print("\nError: No data available to display.")
        return

    display_data(data)

    total_rx = sum(entry['rx'] for entry in data) / (1024*1024*1024)
    total_tx = sum(entry['tx'] for entry in data) / (1024*1024*1024)
    print("\nTotal Bandwidth Usage Across All Interfaces:")
    print(f"Total Received: {total_rx:.2f} GiB")
    print(f"Total Transmitted: {total_tx:.2f} GiB")

    plot_bandwidth(data)

if __name__ == "__main__":
    main()
