import api from "src/api.js"

export async function fetchAll({ commit }) {
    const zones = await api.dns.getZones()
    commit("setZones", zones)
}


export async function createZone({commit}, info){
    const zone = await api.dns.createZone(info)
    commit("addZone", zone)
}

