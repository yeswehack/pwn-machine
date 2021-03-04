import api from "src/api.js"
import { wrapLoading } from "src/store/utils.js"


export const fetchAll = wrapLoading(async ({ commit }) => {
    const [
        containers,
        networks,
        volumes,
        images
    ] = await Promise.all([
        api.docker.getContainers(),
        api.docker.getNetworks(),
        api.docker.getVolumes(),
        api.docker.getImages(),
    ])
    commit("setContainers", containers)
    commit("setNetworks", networks)
    commit("setVolumes", volumes)
    commit("setImages", images)
})


export const pauseContainer = wrapLoading(async ({ commit }, name) => {
    await api.docker.pauseContainer(name)
    commit("pauseContainer", name)
})

export const unpauseContainer = wrapLoading(async ({ commit }, name) => {
    await api.docker.unpauseContainer(name)
    commit("unpauseContainer", name)
})