import socket
from threading import Thread
import pythoncom
import pyHook
from PIL import ImageGrab
import time

SERVER_IP = "127.0.0.1"
PORT = 69
DATA_RECEIVED_SIZE = 1024
OK_DATA_LEN = 2
OK_RESPONSE = "OK"
HOST_NAME_LEN_LEN = 4
NOT_OK_RESPONSE = "SOMETHING WENT WRONG"


class Client(object):
    def __init__(self):
        self.socket = socket.socket()
        self.server_functions_class = ServerFunctions(self.socket)

    def start(self):
        """
        Connecting to the server.
        Sends the hostname to the server.
        """
        self.socket.connect((SERVER_IP, PORT))
        self.send_host_name()

    def send_host_name(self):
        """
        Sends the host name to the server using the host name protocol.
        """
        self.socket.send(str(len(socket.gethostname())).zfill(4))
        if self.socket.recv(OK_DATA_LEN) == OK_RESPONSE:
            self.socket.send(socket.gethostname())
        self.socket.close()

    def receiving_all_msgs(self):
        """
        Opens a thread (self.server_functions_class.receive_msg_from_server_thread).
        """
        receiving_msg_from_server_thread = Thread(target=self.server_functions_class.receive_msg_from_server_thread)
        receiving_msg_from_server_thread.start()


class ServerFunctions(object):
    """
    A Class for the client to use.
    The class holds the functions the clients use to communicate with the server.
    """
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def change_host_name_to_16_bytes(self, host_name):
        """
        Input: The client's host name.
        Output: The client's in 16 bytes.
        """
        client_host_name = socket.gethostname()
        while len(client_host_name) < HOST_NAME_LEN_LEN:
            client_host_name += ""

    def waits_for_data_from_client_to_send_to_the_server(self):
        """
        A function to a thread that waits for data from the client.
        Sends the data that received to the server.
        """
        while True:
            self.client_socket.send(raw_input("insert your msg here..."))

    def get_full_size_data(self, data_len):
        """
        #NOT IN USE
        Input: The length of the data that needs to be received.
        Output: The data that was received.
        description: A function that receives data from the server, and checks to see if all the data has been received.
                     If not, it waits until all the data was received.
        """
        data = self.client_socket.recv(data_len)
        while len(data) < data_len:
            data += self.client_socket.recv(data_len-len(data))
        return data

    def receive_msg_from_server_thread(self):
        """
        A function to a thread that waits for msgs from the server all the time.
        """
        while True:
            data_from_server = self.client_socket.recv(DATA_RECEIVED_SIZE)
            print data_from_server

    @staticmethod
    def screen_shot():
        """
        Takes a screen shot and saves it as a StringIO.
        Return: The data of the image.
        """
        import StringIO
        string_io = StringIO.StringIO()
        ImageGrab.grab().save(string_io, "JPEG")
        return string_io.getvalue()


def lock(event):
    return False


def mouse_lock():
    hm = pyHook.HookManager()
    hm.MouseAll = lock
    hm.HookMouse()
    pythoncom.PumpMessages()


def keyboard_lock():
    hm = pyHook.HookManager()
    hm.KeyAll = lock
    hm.HookKeyboard()
    pythoncom.PumpMessages()


if __name__ == "__main__":
    client = Client()
    client.start()