class Version:
    def __init__(self, major, minor, patch=0):
        if isinstance(major, str):
            if len(major) > 1:
                raise AttributeError()
            major = major.encode("ascii")
        elif isinstance(major, int):
            if major > 255:
                raise AttributeError()
            major = bytes([major])
        elif not isinstance(major, bytes):
            raise AttributeError()

        if isinstance(minor, str):
            if len(minor) > 1:
                raise AttributeError()
            minor = minor.encode("ascii")
        elif isinstance(minor, int):
            if minor > 255:
                raise AttributeError()
            minor = bytes([minor])
        elif not isinstance(minor, bytes):
            raise AttributeError()

        if isinstance(patch, str):
            if len(patch) > 1:
                raise AttributeError()
            patch = patch.encode("ascii")
        elif isinstance(patch, int):
            if patch > 255:
                raise AttributeError()
            patch = bytes([patch])
        elif not isinstance(patch, bytes):
            raise AttributeError()

        self._major = major
        self._minor = minor
        self._patch = patch

    def __lt__(self, other):
        return int(self) < int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    @classmethod
    def fromBytes(cls, data):
        if len(data) != 3:
            raise AttributeError()
        return cls(data[0], data[1], data[2])

    def toBytes(self) -> bytes:
        return bytes(self)

    @property
    def major(self) -> int:
        return self._major[0]

    @property
    def minor(self) -> int:
        return self._minor[0]

    @property
    def patch(self) -> int:
        return self._patch[0]

    def __bytes__(self):
        return self._major + self._minor + self._patch

    def __int__(self):
        return int.from_bytes(bytes(self), "big")

    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
