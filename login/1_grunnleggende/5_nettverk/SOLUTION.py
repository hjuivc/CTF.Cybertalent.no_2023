#!/usr/bin/env python3

import socket
import struct
import select
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 10015

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setblocking(False)
    try:
        conn.connect((TCP_IP, TCP_PORT))
    except BlockingIOError:
        pass

    # Create a list to hold all the connections
    connections = [conn]

    # Create 10 more connections
    for _ in range(10):
        print("Creating new connection")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.setblocking(False)
        try:
            conn.connect((TCP_IP, TCP_PORT))
        except BlockingIOError:
            pass
        connections.append(conn)

    # Initialize a variable to hold the total sum
    total = 0

    # Initialize a variable to hold the time of the last received number
    last_received_time = None

    # Initialize a buffer to hold incoming data
    buffer = ""

    # Check for more data on all connections simultaneously
    while connections:
        ready_to_read, ready_to_write, _ = select.select(connections, connections, [], 5.0)
        for conn in ready_to_read:
            try:
                data = conn.recv(4096)
                if data:
                    # If data is utf-8, add it to the buffer
                    try:
                        buffer += data.decode("utf-8")
                    except UnicodeDecodeError:
                        # If data is a 4-byte integer, add it to the total
                        if len(data) == 4:
                            try:
                                number = struct.unpack('!I', data)[0]
                                total += number
                                print("Received number: ", number)
                                last_received_time = time.time()
                            except struct.error:
                                print("Received invalid data: ", data)
                        else:
                            print("Received non-utf-8 data: ", data)
                    # If the buffer contains a full line, print it and clear the buffer
                    if "\n" in buffer:
                        print("Received data: ", buffer)
                        buffer = ""
                else:
                    print("Connection closed")
                    conn.close()
                    connections.remove(conn)
            except BlockingIOError:
                pass

        # If it has been 2 seconds since the last number was received, send the total sum back to the server
        if last_received_time and time.time() - last_received_time >= 2:
            for conn in ready_to_write:
                try:
                    conn.send(struct.pack('!I', total))
                except BlockingIOError:
                    pass

    # After all numbers have been received and summed, print the total sum
    print("Total sum: ", total)

if __name__ == "__main__":
    main()