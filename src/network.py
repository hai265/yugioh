import websockets
import logging

RECV_SIZE = 1024


class Network:
    def __init__(self) -> None:
        self.buffer = bytearray()

    """Send data to the socket in appropriate socket form"""

    async def send_data(self, sock: websockets, data: bytes):
        """Send data to the connection on the other side of the socket
        :param sock: a socket
        :param data: data in bytes to send to the socket
        """
        await sock.send(data)

    async def recv_data(self, sock: websockets):
        """Recieve data until have enough data in buffer to reconstruct
        Args:
            sock: socket for the network
        """
        data = await sock.recv()
        return data
