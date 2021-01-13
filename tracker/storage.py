from .address import Address

from os import path
import time
import pickle


class BaseStorage:
    def update(self, address: Address, hash: bytes):
        raise NotImplementedError()

    def lookup(self, hash: bytes):
        raise NotImplementedError()

    def reverseLookup(self, address: bytes):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.storage = {}

    def update(self, address: Address, hash: bytes):
        self.storage[hash] = [address, int(time.time())]

    def lookup(self, hash: bytes):
        return self.storage.get(hash)

    def reverseLookup(self, address: bytes):
        result = []
        for key, value in self.storage.items():
            if value[0].getPacked()[:4] == address:
                result.append([key, value[1]])
        return result

    def close(self):
        pass


class PickleStorage(MemoryStorage):
    def __init__(self, file=None, autosave=False):
        super().__init__()
        self.file = file
        self.autosave = autosave
        if self.file is not None and path.exists(self.file) and path.isfile(self.file):
            with open(self.file, "rb") as file:
                try:
                    self.storage = pickle.load(file)
                except:
                    pass

    def save(self):
        if self.file is None:
            return
        with open(self.file, "wb") as file:
            pickle.dump(self.storage, file)

    def update(self, address: Address, hash: bytes):
        super().update(address, hash)
        if self.autosave:
            self.save()

    def close(self):
        self.save()
