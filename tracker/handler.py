import socket
import traceback

import base58

import info
import time

from cli.logger import Logger
from config import config

from .crypto.key import Key
from .storage import BaseStorage
from .address import Address
from utils.version import Version


class Handler:
    def __init__(self, storage: BaseStorage, logger: [Logger, None] = None):
        self.storage = storage
        self.logger = logger

    def __call__(self, addr: Address, fd: socket.socket):
        fd.settimeout(config["timeout"])
        self.handle(addr, fd)

    @staticmethod
    def makeResponse(status: int, body: bytes) -> bytes:
        return info.VERSION.toBytes() + bytes([status & 0xFF]) + body

    @staticmethod
    def readRequest(data: bytes) -> tuple:
        return Version.fromBytes(data[:3]), data[3]

    def handle(self, addr: Address, fd: socket.socket):
        logger = None
        if self.logger: logger = self.logger.create(str(addr))
        try:
            if logger: logger.info(f"Successful connected")
            version, method = self.readRequest(fd.recv(4))
            if logger: logger.info(f"Version: {str(version)}")
            if not version in info.SUPPORTED_VERSIONS:
                if logger: logger.error(f"Unsupported version")
                fd.send(self.makeResponse(254, b""))
            if method == 1:
                if logger: logger.info(f"Method: GET_ADDRESS")
                if logger: logger.info(f"Response: {addr.hostname}")
                fd.send(self.makeResponse(1, addr.getPacked()))
                fd.close()
                return
            elif method == 2:
                if logger: logger.info(f"Method: UPDATE")
                signature = fd.recv(int.from_bytes(fd.recv(2), "big"))
                data = fd.recv(14)
                keysize = fd.recv(2)
                data += keysize + fd.recv(int.from_bytes(keysize, "big"))
                timestamp = int.from_bytes(data[0:8], "big")
                address = Address.fromPacked(data[8:14])
                key = Key.importKey(data[16:])
                if not key.verify(data, signature):
                    if logger: logger.error(f"Response: Signature verification failed")
                    fd.send(self.makeResponse(3, b""))
                    fd.close()
                    return
                if abs(time.time() - timestamp) > config["max_time_distance"]:
                    if logger: logger.error(f"Response: Time verification failed")
                    fd.send(self.makeResponse(2, b""))
                    fd.close()
                    return
                if logger: logger.info(f"DMS Address: {base58.b58encode(key.getHash()).decode('utf-8')}")
                self.storage.update(address, key.getHash())
                if logger: logger.info(f"Response: OK")
                fd.send(self.makeResponse(1, b""))
                fd.close()
                return
            elif method == 3:
                if logger: logger.info(f"Method: LOOKUP")
                id = fd.recv(32)
                if logger: logger.info(f"Lookup query: {base58.b58encode(id).decode('utf-8')}")
                result = self.storage.lookup(id)
                if not result:
                    if logger: logger.error(f"Response: NOT FOUNDED")
                    fd.send(self.makeResponse(2, b""))
                    fd.close()
                    return
                if logger: logger.info(f"Response: {result[0]}")
                fd.send(self.makeResponse(1, result[0].getPacked() + result[1].to_bytes(8, "big")))
                fd.close()
                return
            elif method == 4:
                if logger: logger.info(f"Method: RLOOKUP")
                address = fd.recv(4)
                if logger: logger.info(f"RLookup query: {socket.inet_ntoa(address)}")
                result = self.storage.reverseLookup(address)
                if len(result) == 0:
                    if logger: logger.error(f"Response: Not founded")
                    fd.send(self.makeResponse(2, b""))
                    fd.close()
                    return
                fd.send(self.makeResponse(1, len(result).to_bytes(1, "big")))
                r = ""
                for i in result:
                    r += f"{base58.b58encode(i[0]).decode('utf-8')}, "
                    fd.send(i[0] + i[1].to_bytes(8, "big"))
                if logger: logger.info(f"Response: {r[:-2]}")
                fd.close()
                return
        except:
            if logger: logger.error(f"Response: Server error")
            if logger: logger.error(traceback.format_exc())
            fd.send(self.makeResponse(255, b""))
            fd.close()
            return
