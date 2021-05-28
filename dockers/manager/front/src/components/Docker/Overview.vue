<template>
  <base-overview ref="overview" :loading="$apollo.queries.containers.loading" />
</template>

<script>
import ColorHash from "color-hash";
import cytoscape from "cytoscape";
import fcose from "cytoscape-fcose";
import api from "src/api";
import BaseOverview from "../BaseOverview.vue";

cytoscape.use(fcose);
export default {
  components: { BaseOverview },
  apollo: {
    containers: {
      query: api.docker.containers.LIST_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  methods: {
    renderOveriew(containers) {
      const colorHash = new ColorHash({ saturation: 1 });

      const internet = {
        data: { id: "Internet" },
        position: { x: 0, y: 0 },
        classes: ["internet", "network"]
      };

      const host = {
        data: { id: "host" },
        position: { x: 0, y: 0 },
        classes: ["host", "network"]
      };

      const containerNode = c => ({
        data: { id: c.name },
        style: { "background-color": this.getStatusColor(c.status) },
        classes: ["container"]
      });

      const edge = (container, network, name) => ({
        data: {
          id: `${container.name}${network.name}`,
          name,
          source: container.name,
          target: network.name
        },
        style: { "line-color": colorHash.hex(network.name) }
      });

      const internetEdge = (container, name) => ({
        data: {
          id: `${container.name}$internet$`,
          name,
          source: container.name,
          target: "Internet"
        },
        style: { "line-color": "#ff2200" }
      });

      const hostEdge = (container, name) => ({
        data: {
          id: `${container.name}$host$`,
          name,
          source: container.name,
          target: "host"
        },
        style: { "line-color": "#ff2200" }
      });

      const networkNode = n => {
        const classes = n.name == "host" ? ["host", "network"] : ["network"];
        return {
          data: { id: n.name },
          style: { "border-color": colorHash.hex(n.name) },
          classes
        };
      };
      const elements = [internet, host];

      for (const container of containers) {
        elements.push(containerNode(container));

        for (const port of container.ports) {
          let forwards = [];

          for (const target of port.targets ?? []) {
            forwards.push(`${target}->${port.containerPort}`);
          }
          if (forwards.length) {
            elements.push(internetEdge(container, forwards.join(", ")));
          }
        }
        for (const connection of container.connections) {
          const network = connection.network;
          if (network.name == "host") {
            elements.push(hostEdge(container));
            continue;
          }
          elements.push(networkNode(network));
          elements.push(edge(container, network, connection.ipAddress));
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
              "text-margin-y": -1,
              height: 5,
              shape: "square"
            }
          },
          {
            selector: ".network",
            style: {
              width: 10,
              height: 10,
              shape: "ellipse",
              "background-color": "#1d1d1d",
              "border-width": 1
            }
          },
          {
            selector: ".internet, .host",
            style: {
              width: 10,
              height: 10,
              shape: "ellipse",
              "background-color": "#888888",
              "border-color": "#ff2200"
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
          name: "fcose",
          randomize: true,
          fit: true,
          animate: false
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
