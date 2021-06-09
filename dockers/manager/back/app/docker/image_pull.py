import docker
import asyncio
import random
from uuid import uuid4
from dataclasses import dataclass, field
from collections import defaultdict

from app.api import docker_client
from app.utils import registerMutation, registerSubscription, registerQuery


@dataclass
class Runner:
    name: str
    queues: set[asyncio.Queue] = field(default_factory=set)
    messages: list = field(default_factory=list)
    done: bool = False


class ImagePuller:
    runners: dict[str, Runner] = {}

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
    def has(cls, id):
        return ImagePuller.runners.get(id, None)

    @classmethod
    async def pull(cls, name):
        id = str(uuid4())
        runner = Runner(name)
        cls.runners[id] = runner

        async def pull():
            for message in docker_client.api.pull(name, stream=True, decode=True):
                runner.messages.append(message)
                for queue in runner.queues:
                    queue.put_nowait(message)
                await asyncio.sleep(0)  # release scheduler
            runner.done = True
            for queue in runner.queues:
                queue.put_nowait(None)
            await asyncio.sleep(5)
            cls.runners.pop(id)

        asyncio.ensure_future(pull())
        return id


@registerQuery("dockerImagePulls")
def resolve_pull_image(*_):
    for id, runner in ImagePuller.runners.items():
        yield {"id": id, "name": runner.name}


@registerMutation("pullDockerImage")
async def mutation_pull_image(*_, name):
    id = await ImagePuller.pull(name)
    return {"id": id, "name": name}


@registerSubscription("pullImageProgress")
async def subscribe_to_pull(*_, id):
    if not ImagePuller.has(id):
        return
    async for message in ImagePuller.follow(id):
        yield message
    yield None
