from socket import socket
import logging
RECV_SIZE = 1024


class Network:
    def __init__(self) -> None:
        self.buffer = bytearray()
    """Send data to the socket in appropriate socket form"""
    def send_data(self, sock: socket, data: bytes):
        """Send data to the connection on the other side of the socket
        :param sock: a socket
        :param data: data in bytes to send to the socket
        """
        packet = len(data).to_bytes(4, 'little') + data
        try:
            sock.sendall(packet)
        except Exception as e:
            print(e)
    
    def recv_data(self, sock: socket):
        """Recieve data until have enough data in buffer to reconstruct
        Args:
            sock: socket for the network
        """
        self.buffer += sock.recv(RECV_SIZE)
        size = int.from_bytes(self.buffer[0:4], "little")
        logging.debug("Recieved packet of size " + str(size))
        self.buffer = self.buffer[4:]
        while(len(self.buffer) < size):
            self.buffer += sock.recv(RECV_SIZE)
        data = self.buffer[0:size]
        self.buffer = self.buffer[size:]
        return data