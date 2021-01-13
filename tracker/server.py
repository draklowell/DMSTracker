import socket
import threading

from .address import Address


class Server:
    def __init__(self, address: Address, timeout=1, handler=lambda addr, fd: None):
        self.address = address
        self.timeout = timeout
        self.running = False
        self.handler = handler

        self.socket = socket.create_server(self.address.getSocket())
        self.socket.settimeout(self.timeout)

    def mainloop(self):
        self.running = True
        while self.running:
            try:
                conn, addr = self.socket.accept()
                threading.Thread(target=self.handler, args=(Address.fromSocket(addr), conn)).start()
            except (socket.timeout, OSError):
                continue

    def close(self):
        self.stop()
        self.socket.close()

    def reopen(self):
        self.socket = socket.create_server(self.address.getSocket())
        self.socket.settimeout(self.timeout)

    def stop(self):
        self.running = False
