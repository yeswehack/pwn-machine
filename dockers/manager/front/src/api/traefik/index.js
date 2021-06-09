import GET_ENTRYPOINTS from "./GetEntrypoints.graphql";
import OVERVIEW from "./Overview.graphql";

import services from "./services";
import middlewares from "./middlewares";
import routers from "./routers";
import logs from "./logs";
import entrypoints from "./entrypoints";

export default {
  services,
  middlewares,
  routers,
  logs,
  entrypoints,
  GET_ENTRYPOINTS,
  OVERVIEW
};
