
export function getContainer(state) {
    return name => state.containers.find(c => c.Name == name)
}

export function containers(state) {
    return state.containers
}
export function images(state) {
    return state.images
}
export function networks(state) {
    return state.networks
}
export function volumes(state) {
    return state.volumes
}