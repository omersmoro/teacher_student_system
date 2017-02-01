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


class ClientFunctions(object):
    """
    A Class to organize all the clients functions, for the Server Class to use.
    """
    def __init__(self):
        self.clients_data = []

    def open_chat(self, client_socket):
        """
        Input: The client socket.
        Description: When a new client is connected to the server, 2 threads
                     are opened(self.send_a_msg_to_a_client_thread,
                     self.receive_a_msg_from_a_client).
        """
        client_data = ClientData(client_socket)
        self.clients_data.append(client_data)
        client_data.get_client_host_name()
        receiving_msg_from_client_thread = Thread(target=self.receive_a_msg_from_a_client_thread, args=[client_data])
        receiving_msg_from_client_thread.start()
        sending_msg_to_client_thread = Thread(target=self.send_a_msg_to_a_client_thread, args=[client_data])
        sending_msg_to_client_thread.start()

    @staticmethod
    def send_a_msg_to_a_client_thread(client_data):
        """
        Input: A client's data.
        Description: A function for a thread that waits for the user to
                     insert msgs to send to the client, and sends the msgs.
        """
        client_socket = client_socket = client_data.socket
        while True:
            client_socket.send(raw_input("insert your msg here..."))

    def receive_msgs_from_new_clients_thread(self, client_socket):
        """
        Input: The client socket.
        Description: When a new client is connected to the server, 2 threads
                     are opened(self.send_a_msg_to_a_client_thread,
                     self.receive_a_msg_from_a_client)
        """
        client_data = ClientData(client_socket)
        self.clients_data.append(client_data)
        receiving_msg_from_client_thread = Thread(target=self.receive_a_msg_from_a_client_thread, args=[client_data])
        receiving_msg_from_client_thread.start()

    @staticmethod
    def receive_a_msg_from_a_client_thread(client_data):
        """
        Input: The client socket.
        Description: A function for a thread that waits for
                     data from the client socket and prints it.
        """
        client_socket = client_socket = client_data.socket
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