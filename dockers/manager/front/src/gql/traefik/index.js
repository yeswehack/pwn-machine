import GET_ROUTERS from "./GetRouters.graphql";
import GET_ENTRYPOINTS from "./GetEntrypoints.graphql";
import GET_SERVICES from "./GetServices.graphql";
import GET_MIDDLEWARES from "./GetMiddlewares.graphql";
import CREATE_ROUTER from "./CreateRouter.graphql";
import DELETE_ROUTER from "./DeleteRouter.graphql";
import OVERVIEW from "./Overview.graphql";
import DELETE_MIDDLEWARE from "./DeleteMiddleware.graphql";
import DELETE_SERVICE from "./DeleteService.graphql";
import middlewareMutations from "./MiddlewareMutations.js";
import serviceMutations from "./ServiceMutations.js";

export default {
  GET_ROUTERS,
  DELETE_SERVICE,
  CREATE_SERVICE: serviceMutations.create,
  CREATE_MIDDLEWARE: middlewareMutations.create,
  UPDATE_MIDDLEWARE: middlewareMutations.update,
  DELETE_MIDDLEWARE,
  GET_MIDDLEWARES,
  GET_ENTRYPOINTS,
  CREATE_ROUTER,
  GET_SERVICES,
  OVERVIEW,
  DELETE_ROUTER
};
