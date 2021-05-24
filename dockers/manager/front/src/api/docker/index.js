import GET_CONTAINER_SHELLS from "./GetContainerShells.graphql";
import SPAWN_CONTAINER_SHELL from "./SpawnContainerShell.graphql";
import volumes from "./volumes";
import networks from "./networks";
import containers from "./containers";
import images from "./images";
import logs from "./logs";

export default {
  volumes,
  networks,
  images,
  containers,
  logs,
  GET_CONTAINER_SHELLS,
  SPAWN_CONTAINER_SHELL
};
