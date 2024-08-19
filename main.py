import psutil
import time

def get_network_usage():
    """Get the current network usage."""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def calculate_average_usage(usage_list):
    """Calculate the average network usage from the list of usage records."""
    if not usage_list:
        return 0, 0
    
    total_sent = sum([usage[0] for usage in usage_list])
    total_recv = sum([usage[1] for usage in usage_list])
    
    avg_sent = total_sent / len(usage_list)
    avg_recv = total_recv / len(usage_list)
    
    return avg_sent, avg_recv

def monitor_network(interval=60):
    """Monitor network usage and calculate total and average usage."""
    usage_list = []
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
        
        # Add the usage to the list
        usage_list.append((sent, recv))
        
        # Calculate the average usage per minute
        avg_sent, avg_recv = calculate_average_usage(usage_list)
        
        print(f"Usage in the last {interval} seconds - Sent: {sent / 1024 / 1024:.2f} MB, Received: {recv / 1024 / 1024:.2f} MB")
        print(f"Total usage - Sent: {total_sent / 1024 / 1024:.2f} MB, Received: {total_recv / 1024 / 1024:.2f} MB")
        print(f"Average usage per minute - Sent: {avg_sent / 1024 / 1024:.2f} MB, Received: {avg_recv / 1024 / 1024:.2f} MB")
        print("-" * 50)

if __name__ == "__main__":
    monitor_network()
