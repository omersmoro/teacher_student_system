import socket
from threading import Thread
from PIL import ImageGrab
import time
import base64
import Queue


SERVER_IP = "0.0.0.0"
LOCAL_IP = "127.0.0.1"
CLIENT_PORT = 1025
CLIENT_STREAM_PORT = 1026
LOCAL_PORT = 1027
GUI_STREAM_PORT = 1028
MAX_CLIENTS = 20
DATA_RECEIVED_SIZE = 1024
HOST_NAME_LEN_RECEIVED_SIZE = 4
OK_RESPONSE = "OK"
NOT_OK_RESPONSE = "SOMETHING WENT WRONG"


class Server(object):
    """
    Server Class.
    The server to the teacher-student program.
    The server has many functions for the Treads Class to use, and many functions for the user to use.
    """
    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind((SERVER_IP, CLIENT_PORT))
        self.server_socket.listen(MAX_CLIENTS)

        self.server_stream_socket = socket.socket()
        self.server_stream_socket.bind((SERVER_IP, CLIENT_STREAM_PORT))
        self.server_stream_socket.listen(MAX_CLIENTS)

        self.clients_queues = list()

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
            client_stream_socket, client_address = self.server_stream_socket.accept()
            client_socket, client_address = self.server_socket.accept()
            print "new client"
            self.client_function_class.receive_msgs_from_new_clients(client_socket)

    def creating_client_queue(self):
        #TODO


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
        client_socket = client_data.socket
        while True:
            client_socket.send(raw_input("insert your msg here..."))

    def receive_msgs_from_new_clients(self, client_socket):
        """
        Input: The client socket.
        Description: When a new client is connected to the server, 2 threads
                     are opened(self.send_a_msg_to_a_client_thread,
                     self.receive_a_msg_from_a_client)
        """
        client_data = ClientData(client_socket)
        self.clients_data.append(client_data)
        receiving_a_msg_from_client_thread = Thread(target=self.receive_a_msg_from_a_client_thread, args=[client_data])
        receiving_a_msg_from_client_thread.start()
        sending_a_msg_to_the_client_thread = Thread(target=self.send_a_msg_to_a_client_thread, args=[client_data])
        sending_a_msg_to_the_client_thread.start()

    @staticmethod
    def receive_a_msg_from_a_client_thread(client_data):
        """
        Input: The client socket.
        Description: A function for a thread that waits for
                     data from the client socket and prints it.
        """
        client_socket = client_data.socket
        msg_from_client = None
        while msg_from_client != "":
            msg_from_client = client_socket.recv(DATA_RECEIVED_SIZE)
            print msg_from_client

    @staticmethod
    def screen_shot():
        """
        Takes a screen shot and saves it as a StringIO.
        Return: The data of the image.
        """
        import StringIO
        string_io = StringIO.StringIO()
        ImageGrab.grab().save(string_io, "JPEG")
        return base64.b64encode(string_io.getvalue(), 'utf-8')


class ClientData(object):
    """
    A Class to hold the information of a client.
    """
    def __init__(self, client_socket):
        self.socket = client_socket
        self.hostname = None
        self.change_client_host_name()

    def change_client_host_name(self):
        """
        The clients host name initializes as None.
        The function receiving the client's host name using the host name protocol from the client and
        changes the self.hostname to the clients hostname.
        """
        host_name_len = self.socket.recv(HOST_NAME_LEN_RECEIVED_SIZE)
        self.socket.send(OK_RESPONSE)
        while len(host_name_len) < HOST_NAME_LEN_RECEIVED_SIZE:
            host_name_len += self.socket.recv(HOST_NAME_LEN_RECEIVED_SIZE - host_name_len)
        host_name_len = int(host_name_len)
        self.hostname = self.socket.recv(host_name_len)

    def get_client_host_name(self):
        """
        Output: The client's host name.
        """
        return self.hostname


class SessionWithGui(object):
    """
    A class to communicate with the gui.
    """
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind((LOCAL_IP, LOCAL_PORT))
        self.server_socket.listen()

    def connect_to_gui(self):
        """
        Connect to the gui with the socket.
        """
        try:
            gui_socket, gui_address = self.server_socket.accept()
            return gui_socket

        except socket.error:
            print str(socket.error)

    def send_screen_shot(self):
        """
        Taking the screen shots from the queue and sending them to the gui.
        """


if __name__ == "__main__":
    da_server = Server()
    da_server.start()
    #ClientFunctions.screen_shot()