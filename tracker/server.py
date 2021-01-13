import socket
import threading

from cli.logger import Logger
from .address import Address


class Server:
    def __init__(self, address: Address, timeout=1, handler=lambda addr, fd: None, logger: [Logger, None]=None):
        self.address = address
        self.timeout = timeout
        self.running = False
        self.handler = handler
        self.logger = logger

        self.socket = socket.create_server(self.address.getSocket())
        self.socket.settimeout(self.timeout)
        self.logger.info(f"Started on {self.address}/TCP")

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
        self.logger.info(f"Server stopped")

    def reopen(self):
        self.socket = socket.create_server(self.address.getSocket())
        self.socket.settimeout(self.timeout)
        self.logger.info(f"Restarted on {self.address}/TCP")

    def stop(self):
        self.running = False
