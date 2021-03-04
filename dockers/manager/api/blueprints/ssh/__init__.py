#!/usr/bin/env python
from flask import Blueprint, jsonify, request
from app import redis_client, socketio, docker_client
from uuid import uuid4
from collections import defaultdict
from flask import current_app
from functools import lru_cache
from flask_socketio import join_room, leave_room, Namespace
import os, fcntl, struct, termios, shlex, pty, select, subprocess, sys

bp = Blueprint("ssh", __name__)


BUFF_SIZE = 1024 * 20
LOG_SIZE = 1000


@lru_cache(128)
def get_info_for_uuid(uuid):
    fd = int(redis_client.get(f"/pm/shell/session/{uuid}/fd"))
    name = redis_client.get(f"/pm/shell/session/{uuid}/name")
    return name, fd


class Shell:
    def __init__(self, name, uuid, fd):
        self.uuid = uuid
        self.fd = fd
        self.name = name

    @classmethod
    def cleanup(cls):
        redis_client.delete("/pm/shell/sessions")
        for key in redis_client.keys("/pm/shell/session/*"):
            redis_client.delete(key)

    @classmethod
    def list(cls):
        amount = redis_client.llen("/pm/shell/sessions")
        sessions = redis_client.lrange("/pm/shell/sessions", 0, amount)
        shells = []
        for session in sessions:
            session = session.decode()
            name = redis_client.get(f"/pm/shell/session/{session}/name").decode()
            shells.append({"name": name, "uuid": session})
        return shells

    @classmethod
    def from_uuid(cls, uuid):
        name, fd = get_info_for_uuid(uuid)
        return cls(name, uuid, fd)

    def resize(self, rows, cols, xpix=0, ypix=0):
        winsize = struct.pack("HHHH", rows, cols, xpix, ypix)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    @classmethod
    def start(cls, name, cmd=["bash"]):
        pid, fd = pty.fork()
        if pid == 0:
            subprocess.run(cmd)
            exit(0)
        else:

            shell = cls(name, str(uuid4()), fd)
            socketio.start_background_task(target=lambda: shell._runner())
            shell.created()
            return shell

    def created(self):
        redis_client.rpush("/pm/shell/sessions", self.uuid)
        redis_client.set(f"/pm/shell/session/{self.uuid}/fd", self.fd)
        redis_client.set(f"/pm/shell/session/{self.uuid}/name", self.name)

    def closed(self):
        redis_client.lrem(f"/pm/shell/sessions", 0, self.uuid)
        redis_client.delete(f"/pm/shell/session/{self.uuid}/fd")
        redis_client.delete(f"/pm/shell/session/{self.uuid}/logs")
        socketio.emit("shell_closed", self.uuid, room=self.uuid, namespace="/shell")

    def input(self, data):
        os.write(self.fd, data.encode())

    def emit(self, data):
        socketio.emit("pty_output", {"output": data}, room=self.uuid, namespace="/shell")

    def send_logs(self):
        logs = b""
        for log in redis_client.lrange(
            f"/pm/shell/session/{self.uuid}/logs", 0, LOG_SIZE
        )[::-1]:
            logs += log
        self.emit(logs.decode())

    def output(self, data):
        redis_client.lpush(f"/pm/shell/session/{self.uuid}/logs", data)
        redis_client.ltrim(f"/pm/shell/session/{self.uuid}/logs", 0, LOG_SIZE)
        self.emit(data)

    def _runner(self):
        try:
            while self.fd:
                (data_ready, _, _) = select.select([self.fd], [], [], 0.01)
                if data_ready:
                    data = os.read(self.fd, BUFF_SIZE).decode()
                    self.output(data)
        except OSError:
            pass
        self.closed()


@bp.route("/create/host", methods=["POST"])
def create_shell():
    form = request.get_json()
    name = form.get("name")
    shell = Shell.start(name, ["bash"])
    return jsonify(shell.uuid)


@bp.route("/create/container", methods=["POST"])
def create_container_shell():
    form = request.get_json()
    name = form.get("name")
    cmd = ["docker", "exec", "-t", "-i", "--", name, "sh", "-c", "if which bash; then bash ; else sh ; fi"]
    shell = Shell.start(name, cmd)
    return jsonify(shell.uuid)


@bp.route("/list")
def list_shells():
    return jsonify(Shell.list())


class ShellHandler(Namespace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Shell.cleanup()


    def on_attach(self, data):
        join_room(data["uuid"])

    def on_get_logs(self, data):
        shell = Shell.from_uuid(data["uuid"])
        shell.send_logs()

    def on_resize(self, data):
        shell = Shell.from_uuid(data["uuid"])
        shell.resize(data["rows"], data["cols"])

    def on_pty_input(self, data):
        shell = Shell.from_uuid(data["uuid"])
        shell.input(data["input"])


socketio.on_namespace(ShellHandler("/shell"))
