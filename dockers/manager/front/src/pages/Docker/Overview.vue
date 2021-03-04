<template>
  <div id="overview">
    <div id="graph-container"></div>

    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import ColorHash from "color-hash";
import { mapGetters } from "vuex";
import cytoscape from 'cytoscape';

function isInternetExposed(container) {
  const exposed = [];
  if (!container.NetworkSettings) {
    return false;
  }
  console.log("PORTS", container.NetworkSettings.Ports);
  for (const [name, ports] of Object.entries(container.NetworkSettings.Ports)) {
    if (!ports) continue;
    const [dest, proto] = name.split("/");
    for (const port of ports) {
      if (port.HostPort) {
        exposed.push(`${port.HostPort}->${dest}/${proto}`);
      }
    }
  }
  return exposed.length ? exposed : false;
}

export default {
  props: {
    containers: Array,
    networks: Array,
    volumes: Array
  },
  computed: mapGetters(["loading"]),
  mounted() {
    if (!this.loading) {
      this.init();
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status) {
        case "running":
        case "created":
        case "restarting":
          return "#21BA45";
        case "paused":
          return "#1976D2";
        case "removing":
        case "exited":
        case "dead":
          return "#C10015";
      }
      return "#1976D2";
    },
    init() {
      const colorHash = new ColorHash({ saturation: 1 });

      const edge = (n, f, t) => ({
        data: { id: `${n}${f}${t}`, name: n, source: f, target: t },
        style: { "line-color": colorHash.hex(n) }
      });

      const internetEdge = (e, n) => ({
        data: {
          id: `internet${n}`,
          name: `${e.join(", ")}`,
          source: n,
          target: "Internet"
        },
        style: { "line-color": "red", width: 1 }
      });

      const containerNode = c => ({
        data: { id: c.Name },
        style: { "background-color": this.getStatusColor(c.State.Status) },
        classes: ["container"]
      });

      const internet = {
        data: { id: "Internet" },
        position: { x: 0, y: 0 },
        style: { "border-color": "red", "border-width": ".5" }
      };
      const networks = {};
      const elements = [internet];

      for (const container of this.containers) {
        elements.push(containerNode(container));
        if (!container.NetworkSettings) continue;
        const exposed = isInternetExposed(container);
        if (exposed) {
          elements.push(internetEdge(exposed, container.Name));
        }
        for (const networkName in container.NetworkSettings.Networks) {
          if (!(networkName in networks)) {
            networks[networkName] = [container.Name];
          } else {
            networks[networkName].forEach(n => {
              elements.push(edge(networkName, container.Name, n));
            });
            networks[networkName].push(container.Name);
          }
        }
      }

      const cy = cytoscape({
        container: document.getElementById("graph-container"), // container to render in

        elements: elements,
        wheelSensitivity: 0.5,
        style: [
          {
            selector: "node",
            style: {
              label: "data(id)",
              color: "white",
              "font-size": 5,
              width: 5,
              height: 5,
              shape: "ellipse"
            }
          },
          {
            selector: "edge",
            style: {
              width: 0.5,
              label: "data(name)",
              color: "white",
              "font-size": 0,
              "curve-style": "haystack",
              "haystack-radius": 0.2
            }
          }
        ],
        layout: {
          name: "cose",
          fit: true,
          animate: false,
          nodeDimensionsIncludeLabels: false
        }
      });
      cy.on("mouseover", "edge", function(event) {
        event.target.style("font-size", 4);
      });
      cy.on("mouseout", "edge", function(event) {
        event.target.style("font-size", 0);
      });
    }
  },
  watch: {
    loading(v) {
      console.log("LOADING", v, this.containers);
      if (v == false) {
        this.init();
      }
    }
  }
};
</script>

<style lang="scss" scoped>
#graph-container {
  width: 100%;
  height: calc(100% - 20px);
}
#overview {
  flex-grow: 1;
}
</style>
