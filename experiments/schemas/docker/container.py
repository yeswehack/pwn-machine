# pylint: disable=all
import graphene
from .image import Image
from .client import docker


class Mount(graphene.ObjectType):
    source = graphene.String()
    destination = graphene.String()
    rw = graphene.Boolean()

    def resolve_source(mounted, info):
        return mounted["Source"]

    def resolve_destination(mounted, info):
        return mounted["Destination"]

    def resolve_rw(mounted, info):
        return mounted["RW"]


class BindMount(Mount):
    pass


class VolumeMount(Mount):
    name = graphene.String()
    volume = graphene.Field("schemas.docker.volume.Volume")

    def resolve_name(mounted, info):
        return mounted["Name"]

    def resolve_volume(mounted, info):
        return docker.volumes.get(mounted["Name"])


class Mounts(graphene.ObjectType):
    name = graphene.String()
    volume = graphene.Field("schemas.docker.volume.Volume")
    source = graphene.String()
    destination = graphene.String()
    rw = graphene.Boolean()

    def resolve_source(mounted, info):
        return mounted["Source"]

    def resolve_destination(mounted, info):
        return mounted["Destination"]

    def resolve_rw(mounted, info):
        return mounted["RW"]

    def resolve_name(mounted, info):
        return mounted["Name"] if "Name" in mounted else None

    def resolve_volume(mounted, info):
        return docker.volumes.get(mounted["Name"]) if "Name" in mounted else None


class ConnectedNetwork(graphene.ObjectType):
    name = graphene.String()
    network = graphene.Field("schemas.docker.network.Network")

    def resolve_name(network, info):
        return network

    def resolve_network(network, info):
        return docker.networks.get(network)


class ExposedPort(graphene.ObjectType):
    host_ip = graphene.String()
    host_port = graphene.Int()
    container_port = graphene.Int()
    protocol = graphene.String()


class Container(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    image = graphene.Field(Image)
    created = graphene.DateTime()
    args = graphene.List(graphene.String)
    mounts = graphene.List(Mounts)
    volume_mounts = graphene.List(VolumeMount)
    connected_networks = graphene.List(ConnectedNetwork)
    exposed_ports = graphene.List(ExposedPort)
    status = graphene.String()
    labels = graphene.List("schemas.docker.keyValue.KeyValue")
    environ = graphene.List("schemas.docker.keyValue.KeyValue")
    cmd = graphene.List(graphene.String)
    user = graphene.String(default_value="root")

    def resolve_id(container, info):
        return container.attrs["Id"]

    def resolve_name(container, info):
        name = container.attrs["Name"]
        if name.startswith("/"):
            return name[1:]
        return name

    def resolve_image(container, info):
        return docker.images.get(container.attrs["Image"])

    def resolve_created(container, info):
        return container.attrs["Created"]

    def resolve_mounts(container, info):
        return container.attrs["Mounts"]

    def resolve_volume_mounts(container, info):
        return [m for m in container.attrs["Mounts"] if m["Type"] == "volume"]

    def resolve_connected_networks(container, info):
        networkSettings = container.attrs["NetworkSettings"]
        return [name for name in networkSettings["Networks"]]

    def resolve_exposed_ports(container, info):
        networkSettings = container.attrs["NetworkSettings"]
        ports = []
        for destination, source in networkSettings["Ports"].items():
            # FIXME: What if there is multiple source ?
            host_ip = None if source is None else source[0]["HostIp"]
            host_port = None if source is None else int(source[0]["HostPort"])
            port, protocol = destination.split("/")
            ports.append(
                {
                    "host_ip": host_ip,
                    "host_port": host_port,
                    "container_port": int(port),
                    "protocol": protocol,
                }
            )

        return ports

    def resolve_status(container, info):
        return container.attrs["State"]["Status"]

    def resolve_labels(container, info):
        return container.attrs["Config"]["Labels"].items()

    def resolve_environ(container, info):
        environ = []
        for env in container.attrs["Config"]["Env"]:
            key, _, value = env.partition("=")
            environ.append([key, value])
        return environ

    def resolve_cmd(container, info):
        return container.attrs["Config"]["Cmd"]

    def resolve_user(container, info):
        return container.attrs["Config"]["User"]