import socket
from threading import Thread


SERVER_IP = "127.0.0.1"
PORT = 80
MAX_CLIENTS = 20
DATA_RECEIVED_SIZE = 1024


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
            self.client_function_class.thread_receive_msgs_from_new_clients(client_socket)


class ClientFunctions(object):
    """
    A Class to organize all the clients functions, for the Server Class to use.
    """
    def __init__(self):
        self.clients = []

    def send_msg(self, client_host_name):
        """
        Input: A client host name (socket host name) to check which client to send the msg.
        Description: checks to see which client the server wants to send the msg, and sends the msg.
        """
        for client_socket in self.clients:
            if client_socket.host_name == client_host_name:
                client_socket.send(raw_input("insert your msg here..."))

    def thread_receive_msgs_from_new_clients(self, client_socket):
        """
        When a new client is connected to the server, a thread
        is opened that waits for a msg from a client.
        """
        self.clients.append(client_socket)
        receiving_msg_thread = Thread(target=self.receive_a_msg_from_a_client, args=[client_socket])
        receiving_msg_thread.start()

    @staticmethod
    def receive_a_msg_from_a_client(client_socket):
        while True:
            msg_from_client = client_socket.recv(DATA_RECEIVED_SIZE)
            print msg_from_client


class ClientData(object):
    """
    A Class to hold the information of a client.
    """
    def __init__(self, hostname, socket):
        self.hostname = hostname
        self.socket = socket


if __name__ == "__main__":
    da_server = Server()
    da_server.start()
    if raw_input("send a msg?") == "yes":
        da_server.client_function_class.send_msg(da_server.client_function_class.clients[0].gethostname())