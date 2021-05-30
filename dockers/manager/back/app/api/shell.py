import asyncio
import os
import pty
import select
import struct
import tty
from uuid import uuid4

import psutil

from .docker import docker_client

BUFF_SIZE = 1024
MAX_DATA_SIZE = 1024 * 1024 * 2  # 2Mo


async def create_shell(
    container_name, cmd, *, privileged=None, environment=None, workdir=None, user=None
):
    exec_id = docker_client.api.exec_create(
        container_name,
        cmd,
        stdin=True,
        tty=True,
        privileged=privileged,
        user=user,
        environment=environment,
        workdir=workdir,
    )["Id"]
    meta = {
        "nodeId": exec_id,
        "containerName": container_name,
        "cmd": cmd,
        "running": True,
    }
    socket = docker_client.api.exec_start(exec_id, socket=True)._sock
    reader, writer = await asyncio.open_connection(sock=socket)
    return Shell(container_name, exec_id, reader, writer)


from contextlib import contextmanager


class Shell:
    def __init__(self, container_name, id, reader, writer):
        self.id = id
        self.containerName = container_name
        self.writer = writer
        self.logs = b""
        self.subscribers = set()
        self.exitCode = None
        self.running = True
        asyncio.create_task(self.monitor(reader))

    @property
    def nodeId(self):
        return self.id

    def resize(self, rows, cols):
        if self.running:
            docker_client.api.exec_resize(self.id, rows, cols)

    def write(self, data):
        self.writer.write(data)

    async def monitor(self, reader):
        while True:
            try:
                info = await reader.readexactly(8)
                fd, *_, size = struct.unpack(">bbbbi", info)
                data = await reader.readexactly(size)
            except asyncio.IncompleteReadError:
                break

            self.logs = (self.logs + data)[-MAX_DATA_SIZE:]
            for sub in self.subscribers:
                sub.put_nowait(data)
        status = docker_client.api.exec_inspect(self.id)
        self.exitCode = status["ExitCode"]
        self.running = False
        for sub in self.subscribers:
            sub.put_nowait(None)

    def disconnect(self, con):
        con.stop()
        self.subscribers.remove(con.shell_queue)

    async def connect(self, ws):
        con = ShellConnection(self, ws)
        self.subscribers.add(con.shell_queue)
        return con


class ShellConnection:
    def __init__(self, shell, ws):
        self.shell = shell
        self.ws = ws
        self.shell_queue = asyncio.Queue()
        self.quit_queue = asyncio.Queue()

    def write(self, data):
        self.shell.write(data)

    async def send(self, **kwargs):
        if "stdout" in kwargs:
            kwargs["stdout"] = kwargs["stdout"].decode()
        await self.ws.send_json(kwargs)

    def stop(self):
        self.quit_queue.put_nowait(True)

    async def start(self):
        await self.send(stdout=self.shell.logs)
        if (not self.shell.running):
            await self.send(exit=self.shell.exitCode)
            return

        create_ws_task = lambda: asyncio.create_task(self.ws.receive_json())
        create_shell_task = lambda: asyncio.create_task(self.shell_queue.get())
        create_quit_task = lambda: asyncio.create_task(self.quit_queue.get())

        ws_task = create_ws_task()
        quit_task = create_quit_task()
        shell_task = create_shell_task()

        while True:
            await asyncio.wait(
                (ws_task, shell_task, quit_task),
                return_when=asyncio.FIRST_COMPLETED,
            )
            if quit_task.done():
                shell_task.cancel()
                ws_task.cancel()
                break

            if shell_task.done():
                data = shell_task.result()
                if data is None:
                    await self.send(exit=self.shell.exitCode)
                    quit_task.cancel()
                    ws_task.cancel()
                    break
                    
                await self.send(stdout=data)
                shell_task = create_shell_task()

            if ws_task.done():
                msg = ws_task.result()
                if "stdin" in msg:
                    data = msg["stdin"].encode()
                    self.write(data)
                if "resize" in msg:
                    self.shell.resize(msg["resize"]["rows"], msg["resize"]["cols"])
                ws_task = create_ws_task()
