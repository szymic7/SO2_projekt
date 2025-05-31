import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_sockets = []
previous_messages = []

# Locks (mutexes) for synchronizing access to shared resources
client_sockets_lock = threading.Lock()
previous_messages_lock = threading.Lock()


def receive_message(client_socket, addr):
    """
    Receives messages from a connected client.

    Parameters:
    client_socket (socket.socket): socket connected to a client.
    addr (tuple): address of the client.
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    # Send all the previous messages to the newly connected client
    with previous_messages_lock:
        for hist_msg in previous_messages:
            data = prepare_message(hist_msg)
            client_socket.send(data)

    connected = True
    while connected:
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            msg_length = int(msg_length)
            msg = client_socket.recv(msg_length).decode(FORMAT)
            print(f"Address: {addr}, {msg}")

            # If not a disconnect message, add to chat history
            if msg != DISCONNECT_MESSAGE:
                with previous_messages_lock:
                    previous_messages.append(msg)

                send_messages_to_clients(msg)

            if msg == DISCONNECT_MESSAGE:
                connected = False
        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False

    # Remove client from the list under lock and close the socket
    with client_sockets_lock:
        if client_socket in client_sockets:
            client_sockets.remove(client_socket)
    client_socket.close()


def send_messages_to_clients(msg):
    """
    Sends the message to clients connected to the server.

    Parameters:
    msg (string): message to be sent.
    """
    data = prepare_message(msg)

    # Copy the client list under lock
    with client_sockets_lock:
        clients_copy = client_sockets.copy()
    for client_socket in clients_copy:
        try:
            client_socket.send(data)
        except Exception as e:
            print(f"[SEND ERROR] {e}")
            with client_sockets_lock:
                if client_socket in client_sockets:
                    client_sockets.remove(client_socket)


def start():
    """
    Starts the server and listens for incoming connections.
    """
    print("[SERVER IS STARTING]")
    server.listen()
    server.settimeout(1.0)  # Timeout after 1 second if no connection
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    try:
        while True:
            try:
                client_socket, addr = server.accept()
                # Add new client to the list with synchronization
                with client_sockets_lock:
                    client_sockets.append(client_socket)
                thread = threading.Thread(target=receive_message, args=(client_socket, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
            except socket.timeout:
                continue  # just loop again and check for KeyboardInterrupt
    except KeyboardInterrupt:
        print("\n[SERVER STOPPING] KeyboardInterrupt received. Shutting down.")
        shutdown_server()


def shutdown_server():
    """
    Shuts down the server and all client connections.
    """
    with client_sockets_lock:
        for client_socket in client_sockets:
            try:
                client_socket.send(prepare_message(DISCONNECT_MESSAGE))
                client_socket.shutdown(socket.SHUT_RDWR)  # <-- Clean shutdown
                client_socket.close()
            except:
                pass  # ignore if the connection is already closed
        client_sockets.clear()
    server.close()
    print("[SERVER SHUT DOWN]")


def prepare_message(msg):
    """
    Helper function to format a message to send it to the client.

    Parameters:
    msg (string): message to be formatted.
    """
    message = msg.encode(FORMAT)
    msg_length = len(message)  # number of bytes in the encoded message
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # pads send_length to fit to math the header size
    return send_length + message


if __name__ == '__main__':
    start()
