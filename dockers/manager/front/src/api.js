import Vue from "vue";
import { isValidRule } from "./traefik.js";

function sleep(time) {
  return new Promise(resolve => {
    window.setTimeout(resolve, time);
  });
}

function isObject(item) {
  return item && typeof item === "object" && !Array.isArray(item);
}

function mergeDeep(target, ...sources) {
  if (!sources.length) return target;
  const source = sources.shift();

  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        mergeDeep(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }

  return mergeDeep(target, ...sources);
}

class Fetcher {
  constructor(root, defaultOptions = {}) {
    this.root = root.replace(/\/+$/, "");
    this.defaultOptions = defaultOptions;
  }

  bindStore(store) {
    this.store = store
  }

  async fetch(path, options = {}) {
    const stripedPath = path.replace(/^\/+/, "");
    //this.store && this.store.commit("startLoading")
    const token = this.store.getters.token
    if (!options.hasOwnProperty("headers")) {
      options.headers = {}
    }
    options.headers["Authorization"] = `Bearer ${token}`

    try {
      const r = await fetch(`${this.root}/${stripedPath}`, options);
      if (r.status == 401) {
        this.store && this.store.commit("invalidateToken")
      }
      if (r.status != 200) {
        throw r.status;
      }
      return await r.json();
    } finally {
      //this.store && this.store.commit("stopLoading")
    }
  }

  async largeFetch(path, options = {}) {
    const stripedPath = path.replace(/^\/+/, "");
    const token = this.store.getters.token
    if (!options.hasOwnProperty("headers")) {
      options.headers = {}
    }
    options.headers["Authorization"] = `Bearer ${token}`

    const r = await fetch(`${this.root}/${stripedPath}`, options);
    if (r.status == 401) {
      this.store && this.store.commit("invalidateToken")
    }
    if (r.status != 200) {
      throw r.status;
    }
    return r;

  }
}

class BaseAPI {
  constructor(fetcher) {
    this.fetcher = fetcher
  }

  async fetch(...args) {
    return this.fetcher.fetch(...args)
  }

  async largeFetch(...args) {
    return this.fetcher.largeFetch(...args)
  }

  async get(path, extraOptions = null) {
    const options = mergeDeep({}, this.defaultOptions, extraOptions);
    return this.fetch(path, options);
  }

  async largeGet(path, extraOptions = null) {
    const options = mergeDeep({}, this.defaultOptions, extraOptions);
    return this.largeFetch(path, options);

  }
  async delete(path, extraOptions = null) {
    const deleteOptions = {
      method: "DELETE"
    };
    const options = mergeDeep(
      {},
      this.defaultOptions,
      deleteOptions,
      extraOptions
    );
    return this.fetch(path, options);
  }

  async put(path, data = null, extraOptions = null) {
    const postOptions = {
      method: "PUT"
    }
    if (data != null) {
      postOptions.headers = {
        "Content-Type": "application/json"
      }
      postOptions.body = JSON.stringify(data)
    }
    const options = mergeDeep(
      {},
      this.defaultOptions,
      postOptions,
      extraOptions
    );
    return this.fetch(path, options);
  }
  async post(path, data, extraOptions = null) {
    const postOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    };
    const options = mergeDeep(
      {},
      this.defaultOptions,
      postOptions,
      extraOptions
    );
    return this.fetch(path, options);
  }
}


class DockerApi extends BaseAPI {
  getContainers() {
    return this.get("/docker/containers");
  }
  getNetworks() {
    return this.get("/docker/networks");
  }
  getVolumeFiles(name, path) {
    path = path.replace(/^\/+/, "");
    return this.get(`/docker/volume/${name}/${path}`);
  }

  // FIX ME, it's a bit "hacky"
  getUploadLink(name, path) {
    path = path.replace(/^\/+/, "");
    return `${this.fetcher.root}/docker/upload/${name}/${path}`
  }

  downloadFromVolume(name, path) {
    path = path.replace(/^\/+/, "");
    return this.largeGet(`/docker/download/${name}/${path}`);
  }

  deleteFromVolume(name, path) {
    path = path.replace(/^\/+/, "");
    return this.delete(`/docker/delete/${name}/${path}`);
  }

  getVolumes() {
    return this.get("/docker/volumes");
  }
  getImages() {
    return this.get("/docker/images");
  }

  createVolume(volume) {
    return this.post("/docker/volume", volume);
  }
  createNetwork(network) {
    return this.post("/docker/network", network);
  }

  pauseContainer(name) {
    return this.put(`/docker/container/${name}/pause`)
  }
  unpauseContainer(name) {
    return this.put(`/docker/container/${name}/unpause`)
  }
  startContainer(name) {
    return this.put(`/docker/container/${name}/start`)
  }
  stopContainer(name) {
    return this.put(`/docker/container/${name}/stop`)
  }
  restartContainer(name) {
    return this.put(`/docker/container/${name}/restart`)
  }
}

class TraefikApi extends BaseAPI {
  getEntrypoints() {
    return this.get("/traefik/entrypoints");
  }

  getMiddlewares() {
    return this.get("/traefik/middlewares");
  }
  createMiddleware(middleware) {
    return this.post("/traefik/middlewares", middleware);
  }
  updateMiddleware(name, middleware) {
    return this.post(`/traefik/middlewares/${name}`, middleware);
  }
  deleteMiddleware(name) {
    return this.delete(`/traefik/middlewares/${name}`);
  }

  getServices() {
    return this.get("/traefik/services");
  }
  createService(service) {
    return this.post("/traefik/services", service);
  }
  updateService(name, service) {
    return this.post(`/traefik/services/${name}`, service);
  }
  deleteService(name) {
    return this.delete(`/traefik/services/${name}`);
  }

  getRouters() {
    return this.get("/traefik/routers");
  }
  createRouter(router) {
    return this.post("/traefik/routers", router);
  }
  updateRouter(name, router) {
    return this.post(`/traefik/routers/${name}`, router);
  }
  updateRouterMiddlewares(name, middlewares) {
    return this.post(`/traefik/routers/${name}/middlewares`, middlewares);
  }
  deleteRouter(name) {
    return this.delete(`/traefik/routers/${name}`);
  }
  isValidRule(rule) {
    return isValidRule(rule);
  }
  isValidName(name) {
    return name.match(/^([a-z0-9]|[a-z0-9][a-z0-9\-_]*[a-z0-9])$/gi);
  }

  isValidServiceName(name) {
    return this.isValidName(name);
  }
  isValidMiddlewareName(name) {
    return this.isValidName(name);
  }
  isValidRouterName(name) {
    return this.isValidName(name);
  }
}

class DNSApi extends BaseAPI {
  getZones() {
    return this.get("/dns/zones");
  }

  createZone(zone){
    return this.post("/dns/zones", zone)
  }
}

class ShellApi extends BaseAPI {
  createContainerShell(name) {
    return this.post("/shell/create/container", { name });
  }
  createHostShell(name) {
    return this.post("/shell/create/host", { name });
  }
  getShells() {
    return this.get("/shell/list");
  }
}

class PMApi {
  constructor(fetcher) {
    this.fetcher = fetcher
    this.docker = new DockerApi(fetcher);
    this.traefik = new TraefikApi(fetcher);
    this.dns = new DNSApi(fetcher);
    this.shell = new ShellApi(fetcher);
  }

  bindStore(store) {
    this.fetcher.bindStore(store)
  }
}

const fetcher = new Fetcher("http://127.0.0.1:5000/api", { mode: "cors" })
const api = new PMApi(fetcher);

Vue.prototype.$api = api;
export default api;