<template>
  <base-overview ref='overview' :loading="$apollo.queries.zones.loading" />
</template>

<script>
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import api from "src/api";
import BaseOverview from '../BaseOverview.vue';

export default {
  components: { BaseOverview },
  apollo: {
    zones: {
      query: api.dns.OVERVIEW,
      fetchPolicy: 'cache-and-network',
      update: data => data.dnsZones
    }
  },
  methods: {
    renderOveriew(zones) {
      cytoscape.use(dagre);

      const elements = [];
      const node = (id, label = "", classes = []) => {
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
      const zoneNode = name => node(`z-${name}`, name, ["zone"]);
      const ruleNode = (rule, cls) =>
        node(`ru-${rule.name}-${rule.type}`, `${rule.name} (${rule.type})`, ["rule"]);
      const recordNode = record => node(`re-${record.content}`, record.content, ["record", record.enabled ? 'enabled': 'disabled']);

      for (const zone of zones) {
        elements.push(zoneNode(zone.name));

        for (const rule of zone.rules) {
          elements.push(ruleNode(rule));
          elements.push(edge(`z-${zone.name}`, `ru-${rule.name}-${rule.type}`));

          for (const record of rule.records) {
            elements.push(recordNode(record));
            elements.push(edge(`ru-${rule.name}-${rule.type}`, `re-${record.content}`));
          }

        }
      }
      cytoscape({
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
              width: 8,
              height: 8,
              shape: "ellipse",
              "background-fit": "cover",
              "border-width": 1
            }
          },
          {
            selector: ".enabled",
            style: {
              "background-color": "#1da13c"
            }
          },
          {
            selector: ".disabled",
            style: {
              "background-color": "#c10015"
            }
          },
          {
            selector: ".zone",
            style: {
              "text-margin-y": "-2"
            }
          },
          {
            selector: ".rule",
            style: {
              "text-margin-y": "-2"
            }
          },
          {
            selector: ".record",
            style: {
              "text-valign": "center",
              "text-halign": "right",
              "text-margin-x": "2",
            }
          },
          {
            selector: "edge",
            style: {
              width: 0.1,
              label: "data(label)",
              color: "white",
              "text-rotation": "autorotate",
              "text-margin-y": "-5",
              "font-size": 5,
              "curve-style": "bezier",
              "haystack-radius": 0.1
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
    zones(zones) {
      this.renderOveriew(zones);
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
