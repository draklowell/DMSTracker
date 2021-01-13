from .console import Console


class BaseCommandHandler:
    console = None

    def init(self, console: Console):
        self.console = console

    def __call__(self, command):
        return
