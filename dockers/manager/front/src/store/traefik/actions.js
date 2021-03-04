import api from "src/api.js"
import { wrapLoading } from "src/store/utils.js"

export const fetchAll = wrapLoading(async ({ commit }) => {
    const [
        entrypoints,
        routers,
        services,
        middlewares
    ] = await Promise.all([
        api.traefik.getEntrypoints(),
        api.traefik.getRouters(),
        api.traefik.getServices(),
        api.traefik.getMiddlewares()
    ]);
    commit("setEntrypoints", entrypoints)
    commit("setRouters", routers)
    commit("setServices", services)
    commit("setMiddlewares", middlewares)
})