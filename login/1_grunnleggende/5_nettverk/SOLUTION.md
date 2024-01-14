# Nettverksprogrammering

Så langt har oppgavene dreid seg om å få tilgang til filer på en maskin hvor man allerede har tilgang. Dataangrep starter ofte ved at man må skaffe seg denne tilgangen ved å utnytte en *nettverkstjeneste* som er tilgjengelig på internett.

I denne mappen ligger en server som, etter å ha blitt startet, lytter på port `tcp/10015`. For å få tak i flagget trenger du ikke overflows som i forrige oppgave, men du må vise at du behersker programmeringsferdigheter som å håndtere flere samtidige tilkoblinger og konvertering av binære data.

```sh
$ cp client.py ~/1.6_client.py
$ ./server
$ # I ny terminal:
$ nano ~/1.6_client.py
$ ~/1.6_client.py
$ scoreboard <FLAGG>

login@corax:~$ ~/1.6_client.py
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Creating new connection
Received data:  Dette er en grunnleggende introduksjon til nettverksprogrammering.
Når du har åpnet ti nye tilkoblinger til denne serveren vil du få videre instruksjoner på denne socketen.

Received data:  Du vil nå få tilsendt et 32-bits heltall i `network byte order` i hver av de ti andre sesjonene.
Summer alle, og send resultatet tilbake på denne socketen.
Det er mange måter å konvertere data på. En av dem er `struct.unpack`.

Received number:  13756204
Received number:  155624166
Received number:  222996351
Received number:  199962396
Received number:  95290407
Received number:  105222533
Received number:  247589783
Received number:  16867006
Received number:  130826803
Received number:  213119279
Received data:  Neste melding sendes fordelt over de ti sesjonene.
For å unngå å blokkere mens du leser kan du for eksempel bruke `select.select()` eller `socket.settimeout(0)`.

Received data:  Husk at utf-8 kan ha multi-byte tegn 😊

Received data:

Received data:  ╭────────────────────────────────────────╮

Received data:  │ Gratulerer!                            │

Received data:  │                                        │

Received data:  │ Her er flagget:                        │

Received data:  │                                        │

Received data:  ├────────────────────────────────────────┤

Received data:  │    ed83e02b6da11615dad8eee73dce2cfc    │

Received data:  ╰────────────────────────────────────────╯

```

Her var utgangspunktet på 1.6_client.py:
```python
#!/usr/bin/env python3

import socket
import struct
import select

TCP_IP = "127.0.0.1"
TCP_PORT = 10015

def main():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((TCP_IP, TCP_PORT))
    print(conn.recv(4096).decode("utf-8"))

    # ???

if __name__ == "__main__":
    main()
```

Her var løsnings scriptet:
```python
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
```