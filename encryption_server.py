from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import socket
from Crypto import Random


def main():
    """
    Add Documentation here
    """

    my_socket = socket.socket()
    my_socket.bind(("127.0.0.1", 80))
    my_socket.listen(1)
    client, address = my_socket.accept()
    ciphertext = client.accept()
    obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    obj2.decrypt(ciphertext)


def make_keys(msg):
    """

    """
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    publickey = key.publickey()
    encrypted = publickey.encrypt(msg, 32)

if __name__ == '__main__':
    main()