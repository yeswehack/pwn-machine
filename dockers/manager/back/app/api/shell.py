import asyncio
import fcntl
import os
import pty
import select
import signal
import struct
import subprocess
import termios
import tty
from uuid import uuid4

import psutil

from .docker import docker_client

BUFF_SIZE = 1024
MAX_DATA_SIZE = 1024 * 1024 * 2 # 2Mo

def create_pty(cmd):
    pid, fd = pty.fork()
    if pid == 0:
        subprocess.run(cmd)
        os._exit(0)
    return pid, fd


class ShellManager:
    shells = {}

    def __init__(self):
        raise NotImplemented()

    @classmethod
    def spawn(
        cls,
        container_name,
        cmd,
        *,
        privileged=None,
        environment=None,
        workdir=None,
        user=None,
    ):
        uuid = str(uuid4())

        full_cmd = ["docker", "exec"]

        if privileged:
            full_cmd += ["--privileged"]
        if environment:
            for k, v in environment.items():
                full_cmd += ["--env", f"{k}={v}"]
        if workdir:
            full_cmd += ["-workdir", workdir]
        if user:
            full_cmd += ["--user", user]

        full_cmd += ["-it", container_name, *cmd]
        print(full_cmd)
        pid, fd = create_pty(full_cmd)

        meta = {
            "nodeId": uuid,
            "containerName": container_name,
            "cmd": cmd,
            "fullCmd": full_cmd,
            "pid": pid,
            "fd": fd,
            "running": True
        }

        shell = ContainerShell(fd, meta)
        cls.shells[uuid] = shell
        return shell

    @classmethod
    def get(cls, uuid):
        return cls.shells.get(uuid, None)


    @classmethod
    def remove(cls, uuid):
        del cls.shells[uuid]

    @classmethod
    def all(cls):
        return tuple(cls.shells.values())


class ContainerShell:
    def __init__(self, fd, meta):
        self.meta = meta
        self.fd = fd
        self.logs = b""

    @property
    def running(self):
        return psutil.pid_exist(self.pid)

    def __getattr__(self, name):
        if name in self.meta:
            return self.meta[name]
        return super().__getattr__(name)

    def resize(self, rows, cols):
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def write(self, data):
        return os.write(self.fd, data.encode())

    async def connect(self, ws):
        loop = asyncio.get_running_loop()
        await ws.send_json({"stdout": self.logs.decode()})
        quit_queue = asyncio.Queue()
        stdout_queue = asyncio.Queue()

        def on_stdout_ready():
            try:
                data = os.read(self.fd, BUFF_SIZE)
                self.logs  = (self.logs + data)[-MAX_DATA_SIZE:]
                stdout_queue.put_nowait(data)
            except OSError as e:
                loop.remove_reader(self.fd)
                quit_queue.put_nowait(True)

        stdout_reader = loop.add_reader(self.fd, on_stdout_ready)

        create_ws_task = lambda: asyncio.create_task(ws.receive_json())
        create_stdout_task = lambda: asyncio.create_task(stdout_queue.get())
        create_quit_task = lambda: asyncio.create_task(quit_queue.get())

        ws_task = create_ws_task()
        quit_task = create_quit_task()
        stdout_task = create_stdout_task()

        while True:
            await asyncio.wait(
                (ws_task, stdout_task, quit_task),
                return_when=asyncio.FIRST_COMPLETED,
            )
            if quit_task.done():
                stdout_task.cancel()
                ws_task.cancel()
                ShellManager.remove(self.meta["nodeId"])
                break

            if stdout_task.done():
                data = stdout_task.result().decode()
                asyncio.create_task(ws.send_json({"stdout": data}))
                stdout_task = create_stdout_task()

            if ws_task.done():
                msg = ws_task.result()
                if "stdin" in msg:
                    self.write(msg["stdin"])
                if "resize" in msg:
                    self.resize(msg["resize"]["rows"], msg["resize"]["cols"])
                if "exit" in msg:
                    await quit_queue.put(True)
                    os.kill(self.meta["pid"], signal.SIGKILL)
                ws_task = create_ws_task()


async def handle_shell(ws):
    uuid = ws.path_params.get("uuid")
    shell = ShellManager.get(uuid)
    if shell is None:
        await ws.close()
        return

    try:
        await ws.accept()
        await shell.connect(ws)
        await ws.send_json({"exit": True})
    finally:
        await ws.close()
