from tkinter import *
import queue

# Colors used for the gui components
BLACK = "#000000"
WHITE = "#ffffff"
LIGHT_GRAY = "#c0c1c2"
GRAY = "#919191"
LIGHT_BLUE = "#67c8f5"

# Colors of specific user's messages
USER_COLORS = [
    "#ffffff",  # White
    "#e6194b",  # Red
    "#3cb44b",  # Green
    "#ffe119",  # Yellow
    "#f58231",  # Orange
    "#911eb4",  # Purple
    "#895129",  # Brown
    "#f032e6",  # Magenta
    "#bcf60c",  # Lime
    "#1a27d9",  # Dark Blue
    "#46f0f0",  # Cyan
]

class ClientGUI:
    def __init__(self):
        """
        Initializes a new instance of the ClientGUI.
        """
        self.window = Tk()
        self.window.geometry("400x400+400+200")
        self.window.resizable(False, False)
        self.name = ""
        self.user_colors = {}
        self.user_color_index = 0

        self.entry_name = Entry()  # input for the username
        self.entry_msg = Entry()  # input for the message to be sent
        self.text_messages = Text()  # textarea for the messages to be displayed

        self.running = True

        self.login_screen()  # display login screen
        self.msg_queue = queue.Queue()  # queue of messages to be displayed
        self.recent_sent = None  # store recently sent message to filter echo from the server
        self.poll_queue()  # start checking the queue for new messages to display

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()  # starts the tkinter event loop


    def login_screen(self):
        """
        Displays the login screen.
        """
        self.window.title("Login")
        self.window.configure(bg=WHITE)
        
        # Frame for the login screen
        login_frame = Frame(self.window, bg=WHITE)
        login_frame.place(relwidth=1, relheight=1)
        
        Label(login_frame, 
              text="Welcome to the chat server!",
              font="Helvetica 18 bold",
              bg=WHITE,
              fg=BLACK).pack(pady=(50, 50))
        
        Label(login_frame, 
              text="Type your name and start chatting:",
              font="Helvetica 14",
              bg=WHITE,
              fg=BLACK).pack(pady=(10, 10))
        
        self.entry_name = Entry(login_frame,
                               font="Helvetica 14",
                               bg=WHITE, 
                               fg=BLACK,
                               relief=SOLID,
                               borderwidth=2
                               )
        self.entry_name.pack(pady=(0, 10),  padx=10, ipadx=10, ipady=5)
        self.entry_name.focus()

        Button(login_frame,
               text="START",
               font="Helvetica 12 bold",
               bg=LIGHT_BLUE,
               fg=WHITE,
               relief=FLAT,
               bd=0,
               cursor="hand2",
               command=lambda: self.start_chatting(self.entry_name.get())).pack(side=BOTTOM, anchor='e', pady=30, padx=30, ipadx=5, ipady=5)


    def start_chatting(self, name):
        """
        Starts a client thread to talk to the server.

        Parameters:
        name (string): the name of the user.
        """
        name = name.strip()
        if not name:
            return  # don't proceed when the name is empty

        # Remove login screen widgets
        for widget in self.window.winfo_children():
            widget.destroy()
        self.chat_layout(name)
        from client import talk_to_server
        talk_to_server(self, name)  # Pass the nickname to the server


    def poll_queue(self):
        """
        Updates the GUI when new messages appear in the queue.
        """
        while not self.msg_queue.empty():
            msg = self.msg_queue.get()
            # Filter out echo of our own message from the server
            if self.recent_sent is not None and msg == self.recent_sent:
                self.recent_sent = None
            elif msg != "!DISCONNECT":
                self.display_message(msg)
        self.window.after(100, self.poll_queue)  # run again after 100ms


    def chat_layout(self, name):
        """
        Initializes the chat layout.

        Parameters:
        name (string): the name of the user.
        """
        # Assign a unique color to the current user - always WHITE
        self.name = name.strip()
        self.user_colors[self.name] = USER_COLORS[0]
        color = self.user_colors[self.name]

        self.window.title(f"Chat window for {self.name}")
        self.window.geometry("600x600+400+200")
        self.window.resizable(True, True)
        self.window.configure(bg=LIGHT_GRAY)

        # Header frame displaying nickname
        header_frame = Frame(self.window, bg=LIGHT_GRAY)
        header_frame.pack(fill=X)
        Label(header_frame, 
              text="Chat",
              bg=LIGHT_GRAY,
              fg=BLACK,
              font="Helvetica 14 bold").pack(pady=10)

        # Horizontal line
        line = Frame(self.window, bg=BLACK, height=2)
        line.pack(fill=X, padx=10)

        # Frame for message input
        sending_frame = Frame(self.window, bg=GRAY, height=120)
        sending_frame.pack(fill=X, side=BOTTOM)
        sending_frame.pack_propagate(False)

        # Label displaying the username
        Label(sending_frame,
              text=f"Chatting as: {self.name}",
              bg=GRAY,
              fg=color,
              font="Helvetica 14").pack(anchor="w", padx=15, pady=(15, 0))

        # Input for the message to be sent
        self.entry_msg = Entry(sending_frame,
                               bg=LIGHT_GRAY,
                               fg=BLACK,
                               font="Helvetica 13",
                               bd=0)
        self.entry_msg.pack(side=LEFT, padx=(20, 10), pady=(0, 10), ipady=7, fill=X, expand=True)
        self.entry_msg.focus()

        # Bind Enter key to send message
        self.entry_msg.bind("<Return>", lambda event: self.send_message())

        # Button to send the message
        button_msg = Button(sending_frame,
                            text="Send",
                            font="Helvetica 12 bold",
                            bg=LIGHT_BLUE,
                            fg=WHITE,
                            relief=FLAT,
                            bd=0,
                            cursor="hand2",
                            command=self.send_message)
        button_msg.pack(side=RIGHT, padx=(10, 20), pady=(0, 10), ipadx=5, ipady=5)

        # Frame for chat messages and scrollbar
        chat_frame = Frame(self.window, bg=LIGHT_GRAY)
        chat_frame.pack(padx=10, pady=(5, 0), fill=BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(chat_frame)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)

        # Text area for displaying messages
        self.text_messages = Text(chat_frame,
                                  bg=LIGHT_GRAY,
                                  fg=BLACK,
                                  font="Helvetica 14",
                                  cursor="arrow",
                                  padx=10, pady=10,
                                  bd=0)
        self.text_messages.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_messages.config(state=DISABLED)
        self.text_messages.config(yscrollcommand=scrollbar.set)  # allows scrolling text_messages with a scrollbar
        scrollbar.config(command=self.text_messages.yview)  # scrolls the text_messages


    def send_message(self, event=None):
        """
        Send a message from entry_msg widget to the server.

        Parameters:
        event (tkinter.Event): the tkinter event object; necessary to call the function via bind.
        """
        from client import send
        message = self.entry_msg.get()
        if message:
            full_message = f"{self.name}: {message}"
            send(self.name, message)
            self.entry_msg.delete(0, END)
            # Save sent message to filter the echo from server
            self.recent_sent = full_message
            # Immediately display the message locally
            self.display_message(full_message)


    def display_message(self, msg):
        if not msg:
            return

        self.text_messages.config(state=NORMAL)

        # Try to extract the username from the message
        if ": " in msg:
            username, message_text = msg.split(": ", 1)
            username = username.strip()
            tag = username.replace(" ", "_")  # safe tag name

            # Assign a color if user not seen before
            if username not in self.user_colors:
                color_index = (self.user_color_index % (len(USER_COLORS) - 1)) + 1
                color = USER_COLORS[color_index]
                self.user_colors[username] = color
                self.user_color_index += 1

            # Ensure tag exists for that user (may not if message history is loaded late)
            #if username not in self.text_messages.tag_names():
                #self.text_messages.tag_config(username, foreground=self.user_colors[username], font="Helvetica 14 bold")
            if tag not in self.text_messages.tag_names():
                self.text_messages.tag_config(tag, foreground=self.user_colors[username], font="Helvetica 14 bold")


            # Insert with tag for username
            #self.text_messages.insert(END, f"{username}: ", username)
            self.text_messages.insert(END, f"{username}: ", tag)
            self.text_messages.insert(END, f"{message_text}\n")

        else:
            # If format is unknown, insert as normal
            self.text_messages.insert(END, f"{msg}\n")

        self.text_messages.config(state=DISABLED)
        self.text_messages.yview(END)



    def on_closing(self):
        """
        Disconnects from the server while the window is closed.
        """
        from client import client, DISCONNECT_MESSAGE, FORMAT, HEADER, socket

        self.running = False  # Signal thread to stop

        try:
            # Send disconnect message to the server
            disconnect_msg = DISCONNECT_MESSAGE.encode(FORMAT)
            msg_length = len(disconnect_msg)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(disconnect_msg)

            # Wait for receive thread to exit cleanly
            if hasattr(self, "recv_thread"):
                self.recv_thread.join(timeout=1.0)  # Wait up to 1 second

            # Shutdown to force recv() to unblock
            client.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"[ERROR during shutdown] {e}")
        finally:
            try:
                client.close()
            except:
                pass

        self.window.destroy()
