import socket
import sys
import time
import traceback

import base58

import info
from cli.console import Console
from cli.logger import Logger
from cli.commands import BaseCommandHandler

from tracker.server import Server
from tracker.handler import Handler
from tracker.storage import PickleStorage
from tracker.address import Address

from utils import sizeToString, isInt
from config import config


class CommandHandler(BaseCommandHandler):
    def __call__(self, command):
        try:
            self.handle(command)
        except SystemExit as e:
            raise e
        except:
            shallLogger.error(f"Error while executing command {command}")
            shallLogger.error(traceback.format_exc())

    def handle(self, command):
        args = []
        command = command.split(" ", 1)
        if len(command) > 1:
            command, args = command
            args = args.split(" ")
        else:
            command = command[0]

        if command in ["exit", "q", "quit", "shutdown", "stop"]:
            server.close()
            console.close()
        elif command == "count":
            if len(args) > 0 and isInt(args[0]):
                t = time.time()
                count = 0
                for key, value in storage.storage.items():
                    if t - value[1] <= int(args[0]):
                        count += 1
                shallLogger.info(f"Connected last {args[0]} seconds: {count}")
            else:
                shallLogger.info(f"Connected all time: {len(storage.storage)}")
        elif command == "lookup":
            reverse = False
            if "-r" in args:
                args.remove("-r")
                reverse = True
            if len(args) > 0:
                t = time.time()
                if reverse:
                    result = storage.reverseLookup(socket.inet_aton(args[0]))
                    shallLogger.info("IP ADDRESS\tDMS ADDRESS\tLAST SEEN")
                    for id, value in result:
                        shallLogger.info(f"{args[0]}\t{base58.b58encode(id).decode('utf-8')}\t{int(t-value)} s ago")
                    shallLogger.info("TABLE END")
                else:
                    result = storage.lookup(base58.b58decode(args[0]))
                    shallLogger.info("IP ADDRESS\tDMS ADDRESS\tLAST SEEN")
                    if result:
                        address, value = result
                        shallLogger.info(f"{address.hostname}\t{args[0]}\t{int(t-value)} s ago")
                    shallLogger.info("TABLE END")
            else:
                shallLogger.error("Invalid using, please use: \"lookup [dms address]\" for forward lookup and \"lookup -r [ip address]\" for reverse lookup")
        elif command == "memory":
            shallLogger.info(f"Currently memory used by storage: {sizeToString(sys.getsizeof(storage.storage))}")
        elif command == "list":
            t = time.time()
            if len(args) > 0 and isInt(args[0]):
                t = time.time()
                r = {}
                for key, value in storage.storage.items():
                    if t - value[1] <= int(args[0]):
                        r[key] = value
            else:
                r = storage.storage
            shallLogger.info("IP ADDRESS\tDMS ADDRESS\tLAST SEEN")
            for key, value in r.items():
                shallLogger.info(f"{value[0]}\t{base58.b58encode(key).decode('utf-8')}\t{int(t-value[1])} s ago")
            shallLogger.info("TABLE END")
        elif command == "help":
            shallLogger.info(f"count [time limit] - get count of connected users")
            shallLogger.info(f"lookup [-r] [address] - forward or reverse lookup")
            shallLogger.info(f"memory - get memory used by storage")
            shallLogger.info(f"list [time limit] - list all users")
            shallLogger.info(f"help - open this list")
            shallLogger.info(f"exit ( aliases q, quit, stop, shutdown ) - shutdown server")
        else:
            shallLogger.info(f"Unknown command {command}, please use \"help\" to list commands")


console = Console(CommandHandler())
logger = Logger(console)
logger.togglePrefix(False)
logger.info(f"DMS Tracking Server [Ver. {info.VERSION}] by DrakLowell ( t.me/draklowell )")
logger.info("License GNU General Public License v3.0")
logger.togglePrefix(True)
shallLogger = logger.create("SHELL")
trackerLogger = logger.create("SERVER")

storage = PickleStorage("data.pickle", True)
addr = config["host"].split(":")
server = Server(Address(addr[0], int(addr[1])), handler=Handler(storage, logger=trackerLogger), logger=trackerLogger)
server.mainloop()

console.close()
