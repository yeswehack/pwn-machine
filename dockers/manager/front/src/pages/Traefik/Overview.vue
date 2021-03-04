<template>
  <div id="overview">
    <div id="graph-container"></div>
    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";

export default {
  props: {
    services: Array,
    routers: Array,
    entrypoints: Array,
    middlewares: Array
  },
  computed: mapGetters(["loading"]),
  mounted() {
    if (!this.loading) {
      this.init();
    }
  },
  methods: {
    init() {
      cytoscape.use(dagre);

      const internet = {
        data: { id: "Internet", label: "Internet" },
        classes: ["internet"]
      };
      const elements = [internet];
      const node = (id, label = "", classes = []) => {
        label = label.endsWith("@redis") ? label.slice(0, -6) : label
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
      for (const entrypoint of this.entrypoints) {
        elements.push(entrypointNode(entrypoint.name));
        elements.push(
          edge(
            "Internet",
            `ep-${entrypoint.name}`,
            `${entrypoint.address}/${entrypoint.type}`
          )
        );
      }

      const routerMap = {};

      for (const router of this.routers) {
        elements.push(routerNode(router.name));
        routerMap[router.name] = `r-${router.name}`;

        for (const middleware of router.middlewares || []) {
          elements.push(middlewareNode(middleware));
          elements.push(edge(routerMap[router.name], `m-${middleware}`));
          routerMap[router.name] = `m-${middleware}`;
        }
        for (const entrypoint of router.entryPoints) {
          elements.push(entrypointNode(entrypoint));
          elements.push(
            edge(`ep-${entrypoint}`, `r-${router.name}`, router.rule)
          );
        }
      }

      for (const service of this.services) {
        elements.push(serviceNode(service.name));
        for (const router of service.usedBy || []) {
          elements.push(edge(routerMap[router], `s-${service.name}`));
        }
      }

      const cy = cytoscape({
        container: document.getElementById("graph-container"),

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
              'border-width': 1,
            }
          },
          {
            selector: ".internet",
            style: { "border-color": "red", "border-width": ".5" }
          },
          {
            selector: ".entrypoint",
            style: { shape: "round-rectangle", "background-image": "/icons/log-in-outline.png", "background-fit": "cover" }
          },
          {
            selector: ".router",
            style: { shape: "round-rectangle", "border-color": "#1e54d5", "background-image": "/icons/globe-outline.png", "background-fit": "cover" }
          },
          {
            selector: ".middleware",
            style: { shape: "round-rectangle", "background-image": "/icons/layers.png", "background-fit": "cover" }
          },
          {
            selector: ".service",
            style: { shape: "round-rectangle", "background-image": "/icons/flash.png", "background-fit": "cover" }
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
  },
  watch: {
    loading(v) {
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
