<template>
  <div class="overview">
    <div class="graph-container" ref="graphContainer"></div>
    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import ColorHash from "color-hash";
import cytoscape from "cytoscape";
import gql from "src/gql";

export default {
  apollo: {
    containers: {
      query: gql.docker.GET_CONTAINERS,
      variables() {
        return { name: this.name };
      },
      update: ({ containers }) => containers
    }
  },
  computed: {
    loading() {
      return this.$apollo.queries.containers.loading;
    }
  },
  methods: {
    getStatusColor(status) {
      switch (status.toLowerCase()) {
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
    }
  },
  watch: {
    containers() {
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
        data: { id: c.name },
        style: { "background-color": this.getStatusColor(c.status) },
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
        if (container.exposedPorts.some(p => p.hostPort)) {
          elements.push(
            internetEdge(
              container.exposedPorts.map(
                ep => `${ep.hostPort}->${ep.containerPort}`
              ),
              container.name
            )
          );
        }
        for (const networkName in container.connectedNetworks) {
          if (!(networkName in networks)) {
            networks[networkName] = [container.name];
          } else {
            networks[networkName].forEach(n => {
              elements.push(edge(networkName, container.name, n));
            });
            networks[networkName].push(container.name);
          }
        }
      }

      const cy = cytoscape({
        container: this.$refs.graphContainer,

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
  }
};
</script>

<style lang="scss" scoped>
.graph-container {
  width: 100%;
  height: calc(100% - 20px);
}
.overview {
  flex-grow: 1;
}
</style>
