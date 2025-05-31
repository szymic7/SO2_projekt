import socket
import threading

PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def talk_to_server(gui, nickname):
    """
    Starts a client thread to receive messages from the server and sends the nickname as the first message.

    Parameters:
    gui (ClientGUI): instance of the ClientGUI for which the thread is being created.
    nickname (string): the nickname to give to the client.
    """
    thread = threading.Thread(target=receive_message, args=(client, gui))
    thread.start()
    gui.recv_thread = thread  # Store the thread in the GUI object
    print(f"[CONNECTED] {nickname} connected to the chat server.")


def send(nickname, msg):
    """
    Sends a message to the server with the nickname as prefix.

    Parameters:
    nickname (string): name of the user sending the message.
    msg (string): message to be sent.
    """
    message = f"{nickname}: {msg}"
    message_encoded = message.encode(FORMAT)
    msg_length = len(message_encoded)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Padding to HEADER bytes
    client.send(send_length)
    client.send(message_encoded)


def receive_message(client_socket, gui):
    """
    Receives a message from the server and puts it into the GUI message queue.

    Parameters:
    client_socket (socket.socket): socket connected to the client.
    gui (GUI): instance of the GUI class where the message should be received.
    """
    #connected = True
    #while connected:
    while gui.running:
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client_socket.recv(msg_length).decode(FORMAT)
                gui.msg_queue.put(msg)
                if msg == DISCONNECT_MESSAGE:
                    print(f"[DISCONNECTED] Disconnected from the server.")
                    gui.running = False
                    gui.window.after(0, gui.window.destroy)  # Close GUI from main GUI thread
                    break
                else:
                    print(f"{msg}")
        except OSError as e:
            print(f"[RECV ERROR] {e}")
            break  # Socket closed externally, exit gracefully



if __name__ == '__main__':
    from client_gui import ClientGUI
    g = ClientGUI()
