import Vue from "vue"
export function setContainers(state, containers) {
    state.containers = containers
}

export function setImages(state, images) {
    state.images = images
}

export function setNetworks(state, networks) {
    state.networks = networks
}

export function setVolumes(state, volumes) {
    state.volumes = volumes
}

export function pauseContainer(state, name) {
    const container = state.containers.find(c => c.Name == name)
    if (!container) return
    container.State.Paused = true
    container.State.Status = 'paused'
}
export function unpauseContainer(state, name) {
    const container = state.containers.find(c => c.Name == name)
    if (!container) return
    container.State.Paused = false
    container.State.Status = 'running'
}