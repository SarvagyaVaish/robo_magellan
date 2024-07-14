# Usage
# -----
# On the phone app:
#   - mode: client
#   - protocol: tcp
#   - ip: survy-mac.tail49268.ts.net
#   - port: 8000
#   - enable Log to Stream
#
# Run with:
#   python sensor_server.py
#
# Information about socket streaming:
#   https://stackoverflow.com/a/41383398


import socket
import time
import json


HOST = "survy-mac.tail49268.ts.net"
PORT = 8000


def start_server():
    # Create a socket object and bind
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # Start listening for incoming connections (max 5 queued connections)
    server_socket.listen(5)

    print(f"Listening on \n  host {HOST} \n  port {PORT}")

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")
        print(type(client_socket))

        # Receive data from the client
        while True:
            try:
                start_t = time.perf_counter_ns()
                data = client_socket.recv(8192)  # Buffer size is 1024 bytes
                end_t = time.perf_counter_ns()
                print("----------")
                print(f"  Received: {data}")
                print(f"  Received: {data.decode('utf-8')}")
                print(f"  Took: {(end_t - start_t)/1e9:.5f} secs")
                json_data = json.loads(data.decode("utf-8"))
                print(f"\n\n")

                if not data:
                    break  # If no more data, break out of the loop
            except ConnectionResetError as e:
                print(repr(e))

        # Close the connection
        client_socket.close()
        print(f"Connection from {addr} closed.")


# Run the server
start_server()
