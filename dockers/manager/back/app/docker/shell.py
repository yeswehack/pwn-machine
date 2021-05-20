import shlex


from app.api import ShellManager
from app.utils import createType, registerMutation, registerQuery

DockerContainerShell = createType("DockerContainerShell")


@registerQuery("dockerContainerShells")
def resolve_docker_shells(*_):
    return ShellManager.all()


@registerQuery("dockerContainerShell")
def resolve_docker_shells(id, *_):
    return ShellManager.get(id)


@registerMutation("dockerSpawnContainerShell")
def spawn_container(*_, input):
    container_name = input["containerName"]
    cmd = shlex.split(input["cmd"])
    privileged = input.get("privileged", False)
    environment = input.get("environment", [])
    workdir = input.get("workdir", None)
    user = input.get("user", None)

    shell = ShellManager.spawn(
        container_name,
        cmd,
        privileged=privileged,
        environment=environment,
        workdir=workdir,
        user=user,
    )
    return shell.meta
