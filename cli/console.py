import curses
import threading
import ctypes


class Console:
    def __init__(self, handler, prompt="> "):
        self.handler = handler
        self.handler.init(self)
        self.prompt = prompt

        self.stdscr = curses.initscr()

        curses.echo(True)
        curses.curs_set(False)
        curses.start_color()

        self.stdin = curses.newwin(1, self.stdscr.getmaxyx()[1], self.stdscr.getmaxyx()[0] - 1, 0)
        self.stdout = curses.newwin(self.stdscr.getmaxyx()[0] - 1, self.stdscr.getmaxyx()[1], 0, 0)
        self.stdout.scrollok(True)
        self.thread = threading.Thread(target=self.input)
        self.thread.start()

    def execute(self, command):
        if not command:
            return
        self.handler(command)

    @staticmethod
    def setPair(n, f, b):
        curses.init_pair(n, f, b)

    def createPrompt(self):
        for ch in self.prompt:
            self.stdin.addch(ch)
        self.stdin.refresh()

    def input(self):
        try:
            self.createPrompt()
            while True:
                self.execute(self.stdin.getstr().decode("utf-8"))
                self.stdin.clear()
                self.createPrompt()
        except SystemExit:
            return

    def print(self, text, end="\n", attr=None):
        if attr is not None:
            self.stdout.addstr(text + end, attr)
        else:
            self.stdout.addstr(text + end)
        self.stdout.refresh()

    def close(self):
        # returns id of the respective thread
        thread_id = None
        if hasattr(self.thread, '_thread_id'):
            thread_id = self.thread._thread_id
        for id, thread in threading._active.items():
            if thread is self.thread:
                thread_id = id
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
