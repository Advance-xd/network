import psutil
import time
import json
from datetime import datetime

def get_network_usage():
    """Get the current network usage."""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def monitor_network(interval=60, json_filename="network_usage.json"):
    """Monitor network usage and save data as JSON."""
    usage_data = []
    total_sent, total_recv = 0, 0
    
    while True:
        # Record the starting network usage
        start_sent, start_recv = get_network_usage()
        
        # Wait for the interval (default is 1 minute)
        time.sleep(interval)
        
        # Record the ending network usage
        end_sent, end_recv = get_network_usage()
        
        # Calculate the usage in the last interval
        sent = end_sent - start_sent
        recv = end_recv - start_recv
        
        # Update the total usage
        total_sent += sent
        total_recv += recv
        
        # Record the current time
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Record the data for this interval
        data_point = {
            "timestamp": timestamp,
            "sent_MB": sent / 1024 / 1024,
            "received_MB": recv / 1024 / 1024,
            "total_sent_MB": total_sent / 1024 / 1024,
            "total_received_MB": total_recv / 1024 / 1024,
        }
        usage_data.append(data_point)
        
        # Save the data to a JSON file
        with open(json_filename, "w") as f:
            json.dump(usage_data, f, indent=4)
        
        print(f"Saved data for {timestamp} to {json_filename}")

if __name__ == "__main__":
    monitor_network()
