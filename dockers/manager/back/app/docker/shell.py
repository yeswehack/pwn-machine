import shlex

from . import kv_to_dict
from app.api import create_shell
from app.utils import createType, registerMutation, registerQuery
from starlette.websockets import WebSocketDisconnect
from app.exception import PMException

DockerContainerShell = createType("DockerContainerShell")

shells = {}


@registerQuery("dockerContainerShells")
def resolve_docker_shells(*_):
    return shells.values()


@registerQuery("dockerContainerShellById")
def resolve_docker_shells(id, *_):
    return shells.get(id)


@registerMutation("deleteDockerContainerShell")
def delete_shell(*_, id):
    if id not in shells:
        raise PMException("Invalid id")
    if shells[id].running:
        raise PMException("The shell is still running")
    shells.pop(id)


@registerMutation("spawnDockerContainerShell")
async def spawn_container(*_, input):
    container_name = input["containerName"]
    cmd = shlex.split(input["cmd"])
    privileged = input.get("privileged", False)
    environment = kv_to_dict(input.get("environment", []))
    workdir = input.get("workdir", None)
    user = input.get("user", None)

    shell = await create_shell(
        container_name,
        cmd,
        privileged=privileged,
        environment=environment,
        workdir=workdir,
        user=user,
    )
    shells[shell.id] = shell
    return shell


async def handle_shell(ws):
    uuid = ws.path_params.get("uuid")
    shell = shells.get(uuid)
    if shell is None:
        await ws.close()
        return

    try:
        await ws.accept()
        con = await shell.connect(ws)
        await con.start()
    except WebSocketDisconnect:
        shell.disconnect(con)
    finally:
        await ws.close()
