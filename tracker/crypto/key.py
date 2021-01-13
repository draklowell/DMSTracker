from Crypto.Cipher import PKCS1_v1_5 as Cipher
from Crypto.Signature import PKCS1_v1_5 as Signature
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class NoPrivateKeyError(Exception):
    pass


class Key:
    def __init__(self, key: RsaKey):
        self._key = key
        self._cipher = Cipher.new(self._key)
        self._signature = Signature.new(self._key)

    def isPrivate(self) -> bool:
        return self._key.has_private()

    def isPublic(self) -> bool:
        return not self.isPrivate()

    def getPublic(self):
        return self.__class__(self._key.publickey())

    def getHash(self) -> bytes:
        return SHA256.new(self.getPublic().exportKey("DER")).digest()

    def encrypt(self, data: bytes) -> bytes:
        return self._cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        if not self.isPrivate():
            raise NoPrivateKeyError("There is not private key to decrypt")
        return self._cipher.decrypt(data)

    def sign(self, data: bytes) -> bytes:
        if not self.isPrivate():
            raise NoPrivateKeyError("There is not private key to sign")
        return self._signature.sign(SHA256.new(data))

    def verify(self, data: bytes, sign: bytes) -> bool:
        try:
            return self._signature.verify(SHA256.new(data), sign) in (None, True)
        except (ValueError, TypeError):
            return False

    @classmethod
    def fromPassword(cls, password: str, salt: bytes = b"", keysize: int = 2048, count: int = 10000):
        master_key = PBKDF2(password, salt, count=count)

        def rand(n):
            rand.counter += 1
            return PBKDF2(master_key, f"rand:{rand.counter}", dkLen=n, count=1)

        rand.counter = 0
        return cls(RSA.generate(keysize, randfunc=rand))

    def exportKey(self, format: str = "PEM", passphrase: [str, None] = None) -> bytes:
        return self._key.export_key(format, passphrase)

    @classmethod
    def importKey(cls, data: bytes, passphrase: [str, None] = None):
        return cls(RSA.import_key(data, passphrase))

    @classmethod
    def random(cls, keysize: int = 2048):
        return cls(RSA.generate(keysize))

    def __repr__(self):
        return f"Key({repr(self._key)})"
