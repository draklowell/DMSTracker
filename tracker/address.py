import socket
import re


class Address:
    def __init__(self, hostname: str, port: int):
        if not isinstance(port, int) or not (0 <= port < 2**16):
            raise AttributeError("Port is not 16 bit integer")
        if not isinstance(hostname, str) or not re.fullmatch(r"[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]", hostname):
            raise AttributeError("Invalid hostname format")

        self.hostname = hostname
        self.port = port

    @classmethod
    def fromPacked(cls, packed: bytes):
        if not isinstance(packed, bytes) or len(packed) < 6:
            raise AttributeError("Invalid packed address")
        return cls(socket.inet_ntoa(packed[:4]), int.from_bytes(packed[4:6], "big"))

    @classmethod
    def fromSocket(cls, socket: tuple):
        if not isinstance(socket, tuple) or len(socket) < 2:
            raise AttributeError("Invalid socket host")
        return cls(socket[0], socket[1])

    def __iter__(self) -> iter:
        return iter([self.hostname, self.port])

    def __bytes__(self) -> bytes:
        return socket.inet_aton(self.hostname) + self.port.to_bytes(2, "big")

    def __int__(self) -> int:
        return int.from_bytes(bytes(self), "big")

    def getPacked(self) -> bytes:
        return bytes(self)

    def getSocket(self) -> tuple:
        return tuple(self)

    def getHostname(self) -> str:
        return self.hostname

    def getPort(self) -> int:
        return self.port

    def __eq__(self, other):
        return self.hostname == other.hostname and self.hostname == other.hostname

    def __repr__(self):
        return f"Address({repr(self.hostname)}, {repr(self.port)})"

    def __str__(self):
        return f"{self.hostname}:{self.port}"
