import docker
import asyncio
import random
from uuid import uuid4
from dataclasses import dataclass, field
from collections import defaultdict

from app.api import docker_client
from app.utils import registerMutation, registerSubscription, registerQuery
from . import kv_to_dict


@dataclass
class Runner:
    meta: dict
    queues: set[asyncio.Queue] = field(default_factory=set)
    messages: list = field(default_factory=list)
    done: bool = False


class StreamFollower:
    runners: dict[str, Runner] = {}
    subscribers: set[asyncio.Queue] = set()

    @classmethod
    async def follow(cls, id):
        queue = asyncio.Queue()
        runner = cls.runners.get(id)
        runner.queues.add(queue)

        for message in runner.messages:
            yield message
        if runner.done:
            return
        while message := await queue.get():
            yield message
            queue.task_done()

    @classmethod
    def has(cls, id, check=None):
        if id in cls.runners:
            if check is None:
                return True
            return check(cls.runners[id].meta)
        return False

    @classmethod
    async def subscribe(cls):
        queue = asyncio.Queue()
        cls.subscribers.add(queue)
        while True:
            start_info = await queue.get()
            yield start_info
            queue.task_done()

    @classmethod
    def filter(cls, filter=lambda x: True):
        return [runner for runner in cls.runners.values() if filter(runner.meta)]

    @classmethod
    def create(cls, stream, meta):
        id = str(uuid4())
        meta = {**meta, "id": id}
        runner = Runner(meta)
        cls.runners[id] = runner

        async def start():
            try:
                for message in stream:
                    runner.messages.append(message)
                    for queue in runner.queues:
                        await queue.put(message)
                    await asyncio.sleep(0)  # release loop
            except docker.errors.APIError as e:
                runner.messages.append({"error": e.explanation})
            except Exception as e:
                runner.messages.append({"error": str(e)})
            runner.done = True

            await asyncio.sleep(10)  # Keep the task 10s
            cls.runners.pop(id)

        for sub in cls.subscribers:
            sub.put_nowait(meta)
        asyncio.create_task(start())
        return meta


@registerQuery("dockerStreams")
def resolve_streams(*_):
    return [r.meta for r in StreamFollower.runners.values()]


@registerSubscription("dockerStreamPull")
async def subscribe_to_pull(*_, id):
    if not StreamFollower.has(id, lambda r: r["type"] == "PULL"):
        yield {"done": True}
        return
    async for message in StreamFollower.follow(id):
        yield {**message, "done": False}
    yield {"done": True}


@registerSubscription("dockerStreamBuild")
async def subscribe_to_build(*_, id):
    if not StreamFollower.has(id, lambda r: r["type"] == "BUILD"):
        yield {"done": True}
        return
    async for message in StreamFollower.follow(id):
        yield {**message, "done": False}
    yield {"done": True}


@registerSubscription("dockerStreamStart")
async def resolve_progress_start(*_):
    async for event in StreamFollower.subscribe():
        yield event
