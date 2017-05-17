import socket
from threading import Thread
import pythoncom
import pyHook
from PIL import ImageGrab, Image
import time
import StringIO
import base64
import pickle
import Tkinter
import wx
import win32gui
import win32ui
import win32con
import win32api

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1025
STREAM_PORT = 1028

DATA_RECEIVED_SIZE = 1024
OK_DATA_LEN = 2
OK_RESPONSE = "OK"
NOT_OK_RESPONSE = "SOMETHING WENT WRONG"


class Client(object):
    def __init__(self):
        self.socket = socket.socket()
        self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.session_with_server_class = SessionWithServer(self.socket, self.stream_socket)

    def start(self):
        """
        Connecting to the server.
        """
        self.socket.connect((SERVER_IP, SERVER_PORT))

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
    def __init__(self, client_socket, client_stream_socket):
        self.socket = client_socket
        self.stream_socket = client_stream_socket

    def waits_for_data_from_client_to_send_to_the_server(self):
        """
        A function to a thread that waits for data from the client.
        Sends the data that received to the server.
        """
        while True:
            self.socket.send(raw_input("insert your msg here..."))

    def get_full_size_data(self, data_len):
        """
        #NOT IN USE
        Input: The length of the data that needs to be received.
        Output: The data that was received.
        description: A function that receives data from the server, and checks to see if all the data has been received.
                     If not, it waits until all the data was received.
        """
        data = self.socket.recv(data_len)
        while len(data) < data_len:
            data += self.socket.recv(data_len-len(data))
        return data

    def receive_msg_from_server_thread(self):
        """
        A function to a thread that waits for msgs from the server all the time.
        """
        while True:
            data_from_server = self.socket.recv(DATA_RECEIVED_SIZE)
            if data_from_server == "freeze":
                mouse_lock()
                keyboard_lock()
                #server_stream = Thread(target=self.receive_stream_from_server(), args=[])
                #server_stream.start()
            else:
                print data_from_server

    def send_stream(self):
        """
        Description: Sends the stream of the screen to the server.
        """
        while True:
            image = self.screen_shot()
            #print image
            len_of_img = str(len(image))
            print len_of_img
            self.stream_socket.sendto(len_of_img, (SERVER_IP, STREAM_PORT))
            while image:
                self.stream_socket.sendto(image[:1024], (SERVER_IP, STREAM_PORT))
                image = image[1024:]
            time.sleep(1)

    @staticmethod
    def screen_shot():
        """
        Takes a screen shot and saves it as a StringIO.
        Encoding the data of the image in base 64.
        Return: The data of the image (encoded).
        """
        screen_shot_string_io = StringIO.StringIO()
        ImageGrab.grab().save(screen_shot_string_io, "PNG")
        screen_shot_string_io.seek(0)
        #return base64.b64encode(screen_shot_string_io.getvalue())
        return screen_shot_string_io.read()

    @staticmethod
    def receive_stream_from_server(img_data):
        """

        """
        screen_shot_img = pickle.loads(img_data)
        img = Image.open(screen_shot_img)
        screen_io = StringIO.StringIO()
        img.save(screen_io)
        img = base64.b64decode(img, 'utf-8')
        img.open()


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
    client.session_with_server_class.send_stream()

"""
    string_io = StringIO.StringIO()
    ImageGrab.grab().save(string_io, "JPEG")
    #image_file = StringIO.StringIO(open(string_io.getvalue(), 'rb').read())
    #im = Image.open(image_file)
    print string_io.getvalue()
    root = Tkinter.Tk()
    canvas = Tkinter.Canvas(root, width =1224,height=1000)
    ImageGrab.grab()
    logo = Tkinter.PhotoImage(file='images.jpg')
    canvas.create_image(0, 0, image=logo) #Change 0, 0 to whichever coordinates you need
    root.mainloop()
"""
