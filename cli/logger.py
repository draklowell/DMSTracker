import curses

from .console import Console
from datetime import datetime

INFO = 1
WARNING = 2
ERROR = 3
CRITICAL = 4


class Logger:
    def __init__(self, console: Console, level="", parent=None):
        self.console = console
        self.level = level
        self.parent = parent
        self.console.setPair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.console.setPair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.console.setPair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        self.console.setPair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def isRoot(self):
        return self.parent is None

    def getRoot(self):
        if self.isRoot():
            return self
        else:
            return self.parent.getRoot()

    def getParent(self):
        return self.parent

    def create(self, level):
        return Logger(self.console, level, self)

    def getPrefix(self):
        if self.isRoot():
            return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        else:
            return self.getParent().getPrefix() + f"[{self.level}]"

    def log(self, level, text):
        self.console.print(self.getPrefix() + " " + str(text), attr=curses.color_pair(level))

    def info(self, text):
        self.log(INFO, text)

    def warning(self, text):
        self.log(WARNING, text)

    def error(self, text):
        self.log(ERROR, text)

    def critical(self, text):
        self.log(CRITICAL, text)
