import socket
import threading
import csv
import ipaddress

def send_packet(target_ip, target_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_ip, target_port))
        s.send(message.encode())
        response = s.recv(1024)
        s.close()
        return response.decode()
    except Exception as e:
        return f"Error: {e}"

def test_segment(segment_range):
    segment = ipaddress.ip_network(segment_range)
    message = "Test message from segment testing"
    
    all_ports = list(range(1, 65536))  # all

    results = []
    for ip in segment.hosts():
        ip_str = str(ip)
        for port in all_ports:
            response = send_packet(ip_str, port, message)
            results.append((ip_str, port, response))

    return results

def save_to_csv(results):
    with open("segmentation_test_results.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Target IP", "Port", "Response"])

        for ip, port, response in results:
            csv_writer.writerow([ip, port, response])

def main():
    segment_range = "192.168.1.0/24"  # replace

    test_results = test_segment(segment_range)
    save_to_csv(test_results)

if __name__ == "__main__":
    main()
