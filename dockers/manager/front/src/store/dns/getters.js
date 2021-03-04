
export function zones(state) {
    return state.zones
}

export function records(state) {
    return state.zones.map(z => z.records).flat()
}