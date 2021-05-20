import GET_ROUTERS from "./GetRouters.graphql";
import GET_ENTRYPOINTS from "./GetEntrypoints.graphql";
import GET_SERVICES from "./GetServices.graphql";
import GET_MIDDLEWARES from "./GetMiddlewares.graphql";
import CREATE_HTTP_ROUTER from "./CreateHTTPRouter.graphql";
import CREATE_TCP_ROUTER from "./CreateTCPRouter.graphql";
import CREATE_UDP_ROUTER from "./CreateUDPRouter.graphql";
import UPDATE_HTTP_ROUTER from "./UpdateHTTPRouter.graphql";
import UPDATE_TCP_ROUTER from "./UpdateTCPRouter.graphql";
import UPDATE_UDP_ROUTER from "./UpdateUDPRouter.graphql";
import DELETE_ROUTER from "./DeleteRouter.graphql";
import OVERVIEW from "./Overview.graphql";
import DELETE_MIDDLEWARE from "./DeleteMiddleware.graphql";
import DELETE_SERVICE from "./DeleteService.graphql";
import middlewareMutations from "./MiddlewareMutations.js";
import serviceMutations from "./ServiceMutations.js";

export default {
  GET_ROUTERS,
  CREATE_ROUTER: {
    http: CREATE_HTTP_ROUTER,
    tcp: CREATE_TCP_ROUTER,
    udp: CREATE_UDP_ROUTER
  },
  UPDATE_ROUTER: {
    http: UPDATE_HTTP_ROUTER,
    tcp: UPDATE_TCP_ROUTER,
    udp: UPDATE_UDP_ROUTER
  },
  DELETE_ROUTER,
  DELETE_SERVICE,
  CREATE_SERVICE: serviceMutations.create,
  GET_MIDDLEWARES,
  CREATE_MIDDLEWARE: middlewareMutations.create,
  UPDATE_MIDDLEWARE: middlewareMutations.update,
  DELETE_MIDDLEWARE,
  GET_ENTRYPOINTS,
  GET_SERVICES,
  OVERVIEW
};
