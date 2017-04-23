import socket
from threading import Thread
from PIL import ImageGrab
import time
import base64
import json
import re


SERVER_IP = "0.0.0.0"
LOCAL_IP = "127.0.0.1"

CLIENT_PORT = 1025
CLIENT_STREAM_PORT = 1026

LOCAL_PORT = 1027
LOCAL_STREAM_PORT = 1028

MAX_CLIENTS = 20
DATA_RECEIVED_SIZE = 1024

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

        self.client_function_class = SessionWithClient()

        self.session_with_gui_class = SessionWithGui()

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
            if len(self.client_function_class.clients_data) < MAX_CLIENTS:

                client_stream_socket, client_address = self.server_stream_socket.accept()
                client_socket, client_address = self.server_socket.accept()

                gui_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                gui_client_socket.connect((LOCAL_IP, LOCAL_STREAM_PORT))

                print "new client"
                self.client_function_class.open_chat(client_socket, client_stream_socket,
                                                     client_address, gui_client_socket)
            else:
                print "Max clients reached, can't add more clients."
                break


class SessionWithClient(object):
    """
    A Class to organize all the clients functions, for the Server Class to use.
    """
    def __init__(self):
        self.clients_data = []

    @staticmethod
    def add_client(self):
        """
        Input:
        Description: When a new client connects to the server,
                     this function adds the client's ip to the json file.
        """


    def open_chat(self, client_socket, client_stream_socket, client_address, gui_client_socket):
        """
        Input: The client socket.
        Description: When a new client is connected to the server, 2 threads are
                     opened(self.receive_a_msg_from_a_client,
                     self.connecting_stream_from_client_to_gui).
        """

        client_data = ClientData(client_socket, client_stream_socket, client_address, gui_client_socket)
        self.clients_data.append(client_data)

        receiving_msg_from_client_thread = Thread(target=self.receive_a_msg_from_a_client_thread, args=[client_data])
        receiving_msg_from_client_thread.start()

        receiving_stream_from_client_thread = Thread(target=self.connecting_stream_from_client_to_gui, args=[client_data])
        receiving_stream_from_client_thread.start()

    def send_a_msg_to_a_client(self, ip, text):
        """
        Input: A client's ip address,
               text from the user (from the GUI).
        Description: A function that sends the client the user
                     wants the text the user input in the GUI.
        """
        client_socket = None
        for client_data in self.clients_data:
            if client_data.address == ip:
                client_socket = client_data.socket
        if client_socket:
            client_socket.send(text)

    @staticmethod
    def receive_a_msg_from_a_client_thread(client_data):
        """
        Input: A client's data.
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

    def connecting_stream_from_client_to_gui(self, client_data):
        """
        Input: A client's data.
        Description: A function for a thread that gets the stream of
                     a client and sends it to the gui.
        """
        client_stream_socket = client_data.client_stream_socket
        while True:
            len_of_img = client_stream_socket.recv()
            img = self.get_full_size_data(len_of_img, client_stream_socket)
            client_data.gui_stream_socket.send(len_of_img)
            client_data.gui_stream_socket.send(img)

    @staticmethod
    def get_full_size_data(data_len, client_stream_socket):
        """
        #NOT IN USE
        Input: The length of the data that needs to be received.
        Output: The data that was received.
        description: A function that receives data from the server, and checks to see if all the data has been received.
                     If not, it waits until all the data was received.
        """
        data = client_stream_socket.recv(data_len)
        while len(data) < data_len:
            data += client_stream_socket.recv(data_len-len(data))
        return data


class ClientData(object):
    """
    A Class to hold the information of a client.
    """
    def __init__(self, client_socket, client_stream_socket, client_address, gui_stream_socket):
        self.socket = client_socket
        self.stream_socket = client_stream_socket
        self.address = client_address
        self.gui_stream_socket = gui_stream_socket


class SessionWithGui(object):
    """
    A class to communicate with the gui (the main socket, not the stream sockets).
    """
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind((LOCAL_IP, LOCAL_PORT))
        self.server_socket.listen()

    def connect_to_the_gui(self):
        """
        Connect to the gui with the socket.
        """
        try:
            gui_socket, gui_address = self.server_socket.recv()
            return gui_socket

        except socket.error:
            print str(socket.error)


if __name__ == "__main__":
    da_server = Server()
    da_server.start()