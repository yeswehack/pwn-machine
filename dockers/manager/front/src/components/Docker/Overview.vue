<template>
  <base-overview ref="overview" :loading="$apollo.queries.containers.loading" />
</template>

<script>
import ColorHash from "color-hash";
import cytoscape from "cytoscape";
import api from "src/api";
import BaseOverview from "../BaseOverview.vue";

export default {
  components: { BaseOverview },
  apollo: {
    containers: {
      query: api.docker.GET_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  methods: {
    renderOveriew(containers) {
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

      for (const container of containers) {
        elements.push(containerNode(container));

        for (const port of container.ports) {
          let forwards = [];

          for (const binding of port.hostBindings) {
            forwards.push(
              `${binding.ip}:${binding.port}->${port.containerPort}`
            );
          }
          if (forwards.length) {
            elements.push(internetEdge(forwards, container.name));
          }
        }
        for (const { name: networkName } of container.networks) {
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
        container: this.$refs.overview.getContainer(),

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
    },
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
    containers(containers) {
      this.renderOveriew(containers ?? []);
    }
  }
};
</script>
