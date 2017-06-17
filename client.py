import socket
from threading import Thread
import pythoncom
import pyHook
from PIL import ImageGrab, Image
import time
import StringIO
import base64
import pickle
import win32gui
import win32ui
import win32con
import win32api
import subprocess

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1025
STREAM_TO_SERVER_PORT = 1026
STREAM_FROM_SERVER_PORT = 1030

LOCAL_IP = "127.0.0.1"
CLIENT_IP = "0.0.0.0"

GUI_STREAM_PORT = 1029

DATA_RECEIVED_SIZE = 1024
OK_DATA_LEN = 2
OK_RESPONSE = "OK"
NOT_OK_RESPONSE = "SOMETHING WENT WRONG"

GUI_PATH = r"C:\Heights\Documents\Projects\teacher_student_system\student_gui_windows_forms\student_gui_windows_forms" \
           r"\bin\Debug\student_gui_windows_forms.exe"


class Client(object):
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect((SERVER_IP, SERVER_PORT))
        self.stream_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.stream_from_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.stream_from_server_socket.bind((CLIENT_IP, STREAM_FROM_SERVER_PORT))

        self.gui_server_socket = socket.socket()
        self.session_with_gui_class = SessionWithGui()
        self.session_with_server_class = SessionWithServer(self.socket, self.stream_to_server_socket,
                                                           self.stream_from_server_socket, self.session_with_gui_class)

    def receiving_all_msgs(self):
        """
        Opens a thread (self.server_functions_class.receive_msg_from_server_thread).
        """
        receiving_msg_from_server_thread = Thread(target=self.session_with_server_class.receive_msg_from_server_thread)
        receiving_msg_from_server_thread.start()


class SessionWithServer(object):
    """
    A Class for the client to use.
    The class holds the functions the clients use to communicate with the server.
    """
    def __init__(self, client_socket, stream_to_server_socket, stream_from_server_socket, session_with_gui):
        self.data_socket = client_socket
        self.stream_to_server_socket = stream_to_server_socket
        self.stream_from_server_socket = stream_from_server_socket
        self.session_with_gui_class = session_with_gui

        receiving_stream_from_server = Thread(target=self.connecting_stream_from_server_to_gui)
        receiving_stream_from_server.start()

        receiving_msg_from_server_thread = Thread(target=self.receive_msg_from_server_thread)
        receiving_msg_from_server_thread.start()

    def waits_for_data_from_client_to_send_to_the_server(self):
        """
        #NOT IN USE
        A function to a thread that waits for data from the client.
        Sends the data that received to the server.
        """
        while True:
            self.data_socket.send(raw_input("insert your msg here..."))

    def get_full_size_data(self, data_len):
        """
        Input: The length of the data that needs to be received.
        Output: The data that was received.
        description: A function that receives data from the server, and checks to see if all the data has been received.
                     If not, it waits until all the data was received.
        """
        data = self.stream_from_server_socket.recv(data_len)
        while len(data) < data_len:
            data += self.stream_from_server_socket.recv(data_len-len(data))
        return data

    def receive_msg_from_server_thread(self):
        """
        A function for a thread that waits for msgs from the server all the time.
        """
        while True:
            data_from_server = self.data_socket.recv(DATA_RECEIVED_SIZE)
            if data_from_server == "control":
                self.session_with_gui_class.stream_socket.bind((LOCAL_IP, GUI_STREAM_PORT))
                self.session_with_gui_class.stream_socket.listen(1)
                subprocess.Popen(GUI_PATH)
                #mouse_lock()
                #keyboard_lock()
                print "controlled"
                connecting_stream_from_server_to_gui_thread = Thread(target=self.connecting_stream_from_server_to_gui)
                connecting_stream_from_server_to_gui_thread.start()
            else:
                print 'data_from_server=',data_from_server

    def send_stream(self):
        """
        Description: Sends the stream of the screen to the server.
        """
        while True:
            image = self.screen_shot()
            if type(len(image)) == int:
                len_of_img = str(len(image))
                self.stream_to_server_socket.sendto(len_of_img, (SERVER_IP, STREAM_TO_SERVER_PORT))
                time.sleep(0.03)
                while image:
                    self.stream_to_server_socket.sendto(image[:1024], (SERVER_IP, STREAM_TO_SERVER_PORT))
                    image = image[1024:]
                time.sleep(0.03)
            else:
                print type(len(image))
                time.sleep(0.03)

    @staticmethod
    def screen_shot():
        """
        Takes a screen shot and saves it as a StringIO.
        Return: The data of the image.
        """
        screen_shot_string_io = StringIO.StringIO()
        ImageGrab.grab().save(screen_shot_string_io, "PNG")
        screen_shot_string_io.seek(0)
        return screen_shot_string_io.read()

    def connecting_stream_from_server_to_gui(self):
        """
        #WHEN TO STOP?
        Input: A client's data.
        Description: A function for a thread that gets the stream of
                     a client and sends it to the gui.
        """
        while True:
            try:
                len_of_img, client_address = self.stream_from_server_socket.recvfrom(DATA_RECEIVED_SIZE)
                len_of_img = self.change_int_to_7_length(len_of_img)
                print len_of_img
                img = self.get_full_size_data(int(len_of_img))

                self.session_with_gui_class.send_data(len_of_img)
                time.sleep(0.03)
                self.session_with_gui_class.send_data(img)
                time.sleep(0.03)

            except ValueError:
                print ValueError

    @staticmethod
    def change_int_to_7_length(num):
        """
        Input: A number.
        Output: The number (string).
        Description: Changes the number length to 8 by adding 0s to the start of it
        """
        while len(num) < 7:
            num = "0" + str(num)
        return num


class SessionWithGui(object):
    """
    A class to communicate with the gui.
    """
    def __init__(self):
        self.stream_socket = socket.socket()

    def send_data(self, data):
        """
        Receives: data.
        Description: Sends the data to the gui in chunks of 1024 bytes.
        """
        while data:
            self.stream_socket.send(data[:1024])
            data = data[1024:]


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
    client.session_with_server_class.send_stream()
