import socket
from threading import Thread

SERVER_IP = "127.0.0.1"
PORT = 80
DATA_RECEIVED_SIZE = 1024


class Client(object):
    def __init__(self):
        self.socket = socket.socket()

    def connecting_to_the_server(self):
        """
        Connecting to the server.
        """
        self.socket.connect((SERVER_IP, PORT))
        self.socket.send(socket.gethostname())

    def sending_a_msg(self):
        """
        Sending a msg to the server.
        """
        self.socket.send(raw_input("insert your msg here..."))

    def receive_msg_from_server(self):
        """
        A thread that waits for msgs from the server all the time.
        """
        self.socket.recv(DATA_RECEIVED_SIZE)

if __name__ == "__main__":
    da_clientos = Client()
    #da_clientos.connecting_to_the_server()
    #da_clientos.receive_msg_from_server()