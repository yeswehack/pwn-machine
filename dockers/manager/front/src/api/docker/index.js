import GET_CONTAINER_SHELLS from "./GetContainerShells.graphql";
import SPAWN_CONTAINER_SHELL from "./SpawnContainerShell.graphql";
import volume from "./volume";
import network from "./network";
import container from "./container";
import image from "./image";

export default {
  volume,
  network,
  image,
  container,
  GET_CONTAINER_SHELLS,
  SPAWN_CONTAINER_SHELL
};
