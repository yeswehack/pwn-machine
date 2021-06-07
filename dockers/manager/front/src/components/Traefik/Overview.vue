<template>
  <base-overview
    ref="overview"
    :loading="$apollo.queries.entrypoints.loading"
  />
</template>

<script>
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import api from "src/api";
import BaseOverview from "../BaseOverview.vue";

export default {
  components: { BaseOverview },
  apollo: {
    entrypoints: {
      query: api.traefik.OVERVIEW,
      update: data => data.traefikEntrypoints
    }
  },
  watch: {
    entrypoints(entrypoints) {
      this.renderOverview(entrypoints ?? []);
    }
  },
  methods: {
    renderOverview(entrypoints) {
      cytoscape.use(dagre);

      const internet = {
        data: { id: "Internet", label: "Internet" },
        classes: ["internet"]
      };
      const elements = [internet];
      const node = (id, label = "", classes = []) => {
        label = label.endsWith("@redis") ? label.slice(0, -6) : label;
        return {
          data: { id, label },
          classes
        };
      };

      const edge = (source, target, label = "") => ({
        data: {
          id: `${source}-${target}`,
          label,
          source,
          target
        }
      });
      const entrypointNode = name => node(`ep-${name}`, name, ["entrypoint"]);
      const routerNode = name => node(`r-${name}`, name, ["router"]);
      const serviceNode = name => node(`s-${name}`, name, ["service"]);
      const middlewareNode = name => node(`m-${name}`, name, ["middleware"]);

      for (const entrypoint of entrypoints) {
        elements.push(entrypointNode(entrypoint.name));
        elements.push(
          edge("Internet", `ep-${entrypoint.name}`, `${entrypoint.address}`)
        );

        for (const router of entrypoint.usedBy) {
          elements.push(routerNode(router.name));
          elements.push(
            edge(`ep-${entrypoint.name}`, `r-${router.name}`, router.rule)
          );

          let lastMiddleware = `r-${router.name}`;
          for (const { name: middleware } of router.middlewares || []) {
            elements.push(middlewareNode(middleware));
            elements.push(edge(lastMiddleware, `m-${middleware}`));
            lastMiddleware = `m-${middleware}`;
          }

          elements.push(serviceNode(router.service.name));
          elements.push(edge(lastMiddleware, `s-${router.service.name}`));
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
              label: "data(label)",
              color: "white",
              "font-size": 5,
              width: 10,
              height: 10,
              "text-margin-y": "-2",
              shape: "ellipse",
              "background-fit": "cover",
              "border-width": 1
            }
          },
          {
            selector: ".internet",
            style: { "border-color": "red", "border-width": ".5" }
          },
          {
            selector: ".entrypoint",
            style: {
              shape: "round-rectangle",
              "background-image": "/icons/log-in-outline.png"
            }
          },
          {
            selector: ".router",
            style: {
              shape: "round-rectangle",
              "background-image": "/icons/globe-outline.png"
            }
          },
          {
            selector: ".middleware",
            style: {
              shape: "round-rectangle",
              "background-image": "/icons/layers.png"
            }
          },
          {
            selector: ".service",
            style: {
              shape: "round-rectangle",
              "background-image": "/icons/flash.png"
            }
          },
          {
            selector: "edge",
            style: {
              width: 0.5,
              label: "data(label)",
              color: "white",
              "text-rotation": "autorotate",
              "text-margin-y": "-5",
              "font-size": 5,
              "curve-style": "bezier",
              "haystack-radius": 0.2
            }
          }
        ],
        layout: {
          name: "dagre",
          rankDir: "LR",
          fit: true,
          nodeDimensionsIncludeLabels: true
        }
      });
    }
  }
};
</script>
