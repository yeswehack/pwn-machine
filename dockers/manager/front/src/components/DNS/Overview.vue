<template>
  <q-tree
    v-if="overviewTree"
    class="full-width"
    :nodes="overviewTree"
    :expanded.sync="expanded"
    node-key="id"
  />
</template>

<script>
import api from "src/api";

export default {
  apollo: {
    overviewTree: {
      query: api.dns.OVERVIEW,
      fetchPolicy: "cache-and-network",
      update(data) {
        const zones = data.dnsZones;
        this.expanded.splice(0, this.expanded.length);
        return zones.map(zone => {
          const zoneId = zone.name;
          const rules = (zone.rules ?? []).map(rule => {
            const ruleId = `${zoneId}-${rule.type}.${rule.name}`;
            const records = rule.records.map((record, idx) => {
              const recordId = `${ruleId}-${idx}`;
              return {
                label: record.content,
                id: recordId,
                icon: "trip_origin",
                iconColor: record.enabled ? "positive" : "negative"
              };
            });
            return {
              label: `${rule.type} - ${rule.name}`,
              id: ruleId,
              icon: "eva-book",
              children: records
            };
          });
          this.expanded.push(zoneId);
          return {
            label: zone.name,
            children: rules,
            icon: "eva-home-outline",
            id: zoneId
          };
        });
      }
    }
  },
  data: () => ({ expanded: [] })
};
</script>
