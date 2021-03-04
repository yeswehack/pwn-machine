import Vue from "vue"
export function setZones(state, zones) {
    state.zones = zones
}

export function addZone(state, zone){
    state.zones.push(zone)
}