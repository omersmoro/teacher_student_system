import socket
from threading import Thread


SERVER_IP = "127.0.0.1"
PORT = 80
MAX_CLIENTS = 20
DATA_RECEIVED_SIZE = 1024
HOST_NAME_LEN_RECEIVED_SIZE = 4


class Server(object):
    """
    Server Class.
    The server to the teacher-student program.
    The server has many functions for the Treads Class to use, and many functions for the user to use.
    """
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket = socket.socket()
        self.server_socket.bind((SERVER_IP, PORT))
        self.server_socket.listen(MAX_CLIENTS)
        self.client_function_class = ClientFunctions()

    def start(self):
        """
        Starting the program.
        Opens a thread (self.accept_client).
        """
        waiting_for_clients = Thread(target=self.accept_client)
        waiting_for_clients.start()

    def accept_client(self):
        """
        A function to a thread that always connects a client to the server.
        Adds the client to the clients list.
        """
        while True:
            client_socket, client_address = self.server_socket.accept()
            print "new client"
            self.client_function_class.receive_msgs_from_new_clients_thread(client_socket)

    def open_chat(self):
        """
        """


class ClientFunctions(object):
    """
    A Class to organize all the clients functions, for the Server Class to use.
    """
    def __init__(self):
        self.clients_data = []

    def send_msg_thread(self, client_host_name):
        """
        Input: A client host name to check which client to open a chat with.
        Description: checks to see with which client the server wants to open a chat,
                     and opens the chat.
        """
        for client_socket in self.clients_data:
            if client_socket.host_name == client_host_name:
                client_socket.send(raw_input("insert your msg here..."))

    def receive_msgs_from_new_clients_thread(self, client_socket):
        """
        Input: The client socket.
        Description: When a new client is connected to the server, a thread
                     is opened that waits for a msg from a client.
        """
        client_data = ClientData(client_socket)
        self.clients_data.append(client_data)
        receiving_msg_from_client_thread = Thread(target=self.receive_a_msg_from_a_client, args=[client_data])
        receiving_msg_from_client_thread.start()

    @staticmethod
    def receive_a_msg_from_a_client(client_data):
        """
        Input: The client socket.
        Description: A function for a thread that waits for
                     data from the client socket and prints it.
        """
        client_data.get_client_host_name()
        client_socket = client_data.socket
        while True:
            msg_from_client = client_socket.recv(DATA_RECEIVED_SIZE)
            print msg_from_client


class ClientData(object):
    """
    A Class to hold the information of a client.
    """
    def __init__(self, socket):
        self.socket = socket
        self.hostname = None

    def get_client_host_name(self):
        """
        Output: The client's host name.
        Receiving the client's host name using the host name protocol.
        """
        host_name_len = self.socket.recv(HOST_NAME_LEN_RECEIVED_SIZE)
        while len(host_name_len) < HOST_NAME_LEN_RECEIVED_SIZE:
            host_name_len += self.socket.recv(HOST_NAME_LEN_RECEIVED_SIZE - host_name_len)
        host_name_len = int(host_name_len)
        self.hostname = self.socket.recv(host_name_len)
        return self.hostname


if __name__ == "__main__":
    da_server = Server()
    da_server.start()
    if raw_input("send a msg?") == "yes":
        da_server.client_function_class.send_msg(da_server.client_function_class.clients[0].gethostname())