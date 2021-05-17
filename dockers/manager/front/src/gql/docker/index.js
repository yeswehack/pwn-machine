import GET_CONTAINERS from "./GetContainers.graphql";
import GET_CONTAINER_SHELLS from "./GetContainerShells.graphql";
import GET_IMAGES from "./GetImages.graphql";
import GET_NETWORKS from "./GetNetworks.graphql";
import SEARCH_IMAGE from "./SearchImage.graphql";
import SEARCH_IMAGE_TAG from "./SearchImageTag.graphql";

export default {
  SEARCH_IMAGE,
  SEARCH_IMAGE_TAG,
  GET_CONTAINER_SHELLS,
  GET_CONTAINERS,
  GET_IMAGES,
  GET_NETWORKS
};
