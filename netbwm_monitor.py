import os
import psutil
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Function to gather network usage statistics for all interfaces
def get_network_stats():
    return psutil.net_io_counters(pernic=True)

# Function to calculate rate in bits per second
def calculate_rate(bytes_before, bytes_after, duration):
    bytes_diff = bytes_after - bytes_before
    bits = bytes_diff * 8
    return bits / duration

# Function to display network statistics
def display_stats(interface, rx_rate, tx_rate):
    units = ['bit/s', 'Kbit/s', 'Mbit/s', 'Gbit/s']
    
    def format_rate(rate):
        unit_index = 0
        while rate >= 1000 and unit_index < len(units) - 1:
            rate /= 1000
            unit_index += 1
        return f"{rate:.2f} {units[unit_index]}"

    print(f"\nInterface: {interface}")
    print("+----------------------+--------------------+")
    print("| Bandwidth Rates      |                    |")
    print("+----------------------+--------------------+")
    print(f"| Receive rate:        | {format_rate(rx_rate):<18} |")
    print(f"| Transmit rate:       | {format_rate(tx_rate):<18} |")
    print("+----------------------+--------------------+")

# Main function
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

    # Get sleep duration from user
    while True:
        try:
            sleep_duration = float(input("Enter the data collection interval in seconds (e.g., 1 for hourly report): "))
            if sleep_duration > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    if report_type == '-h':
        # Hourly Report
        for hour in range(24):
            stats_before = get_network_stats()
            start_time = time.time()
            time.sleep(sleep_duration)  # Use configurable sleep duration
            end_time = time.time()
            duration = end_time - start_time
            stats_after = get_network_stats()
            
            for interface in stats_before:
                if interface in stats_after:
                    try:
                        rx_before = stats_before[interface].bytes_recv
                        tx_before = stats_before[interface].bytes_sent
                        rx_after = stats_after[interface].bytes_recv
                        tx_after = stats_after[interface].bytes_sent
                        
                        rx_rate = calculate_rate(rx_before, rx_after, duration)
                        tx_rate = calculate_rate(tx_before, tx_after, duration)
                        display_stats(interface, rx_rate, tx_rate)
                    except AttributeError:
                        print(f"Skipping interface '{interface}' due to missing data.")
    elif report_type == '-d':
        # Daily Report
        stats_before = get_network_stats()
        start_time = time.time()
        time.sleep(86400)  # Simulate data collection for a day
        end_time = time.time()
        duration = end_time - start_time
        stats_after = get_network_stats()
        
        for interface in stats_before:
            if interface in stats_after:
                try:
                    rx_before = stats_before[interface].bytes_recv
                    tx_before = stats_before[interface].bytes_sent
                    rx_after = stats_after[interface].bytes_recv
                    tx_after = stats_after[interface].bytes_sent
                    
                    rx_rate = calculate_rate(rx_before, rx_after, duration)
                    tx_rate = calculate_rate(tx_before, tx_after, duration)
                    display_stats(interface, rx_rate, tx_rate)
                except AttributeError:
                    print(f"Skipping interface '{interface}' due to missing data.")
    elif report_type == '-m':
        # Monthly Report
        stats_before = get_network_stats()
        start_time = time.time()
        time.sleep(2592000)  # Simulate data collection for a month (30 days)
        end_time = time.time()
        duration = end_time - start_time
        stats_after = get_network_stats()
        
        for interface in stats_before:
            if interface in stats_after:
                try:
                    rx_before = stats_before[interface].bytes_recv
                    tx_before = stats_before[interface].bytes_sent
                    rx_after = stats_after[interface].bytes_recv
                    tx_after = stats_after[interface].bytes_sent
                    
                    rx_rate = calculate_rate(rx_before, rx_after, duration)
                    tx_rate = calculate_rate(tx_before, tx_after, duration)
                    display_stats(interface, rx_rate, tx_rate)
                except AttributeError:
                    print(f"Skipping interface '{interface}' due to missing data.")

if __name__ == "__main__":
    main()