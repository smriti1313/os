# THIS IS THE SERVER SIDE CODE WHICH WILL OPEN A CONNECTION AND ONCE CONNECTED, WILL READ THE FILE MENTIONED BY THE CLIENT
import socket
import threading
from analysis import analysis_thread
from clientHandler import handle_client
from dataStructures import SharedList
import argparse

shared_list = SharedList()
list_lock = threading.Lock()
connection_order = 0
connection_order_lock = threading.Lock()
pattern_frequencies = {}
connection_order_container = [0]

def main(port, search_pattern):  # Added a search_pattern argument
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(5)
    print(f"Server started on port {port}")

    # Start the analysis thread using the specified search pattern
    threading.Thread(target=analysis_thread, args=(shared_list, search_pattern)).start()

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(
            client, shared_list, list_lock, connection_order_lock, connection_order_container))
        client_handler.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for book transfer.')
    parser.add_argument('-l', '--port', type=int, help='Port to start the server on.', required=True)
    parser.add_argument('-p', '--pattern', type=str, help='Pattern to search in the book.', required=True)
    args = parser.parse_args()
    main(args.port, args.pattern)  # Passing the port and search pattern arguments
