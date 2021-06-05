<template>
  <base-table
    ref="table"
    name="zone"
    row-key="name"
    :query="$apollo.queries.zones"
    :data="zones"
    :columns="columns"
    @create="createZone"
    @clone="cloneZone"
    @delete="deleteZone"
  >
    <template #details="{row}">
      <zone-details :value="row" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ZoneDialog from "src/components/DNS/Zone/Dialog.vue";
import ZoneDetails from "src/components/DNS/Zone/Details.vue";

import api from "src/api";

export default {
  components: { BaseTable, ZoneDetails },
  apollo: {
    zones: {
      query: api.dns.zones.LIST_ZONES,
      update: data => data.dnsZones
    }
  },
  methods: {
    createZone() {
      this.$q.dialog({
        component: ZoneDialog,
        parent: this
      });
    },
    cloneZone(zone) {
      this.$q.dialog({
        component: ZoneDialog,
        parent: this,
        zone
      });
    },
    deleteZone(zone) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${zone.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.dns.zones.DELETE_ZONE,
            variables: { nodeId: zone.nodeId },
            refetchQueries: [{ query: api.dns.zones.LIST_ZONES }],
            message: `${zone.name} deleted`
          });
        });
    }
  },
  data() {
    const field = (name, opt = {}) => ({
      name: name,
      align: "left",
      label: name,
      field: name,
      sortable: true,
      autoWidth: true,
      ...opt
    });
    const soaField = (name, opt = {}) =>
      field(name, { field: r => r.soa[name], ...opt });
    const columns = [
      field("name", { autoWidth: false }),
      soaField("nameserver", { autoWidth: false }),
      soaField("postmaster", { autoWidth: false }),
      field("serial"),
      soaField("refresh"),
      soaField("retry"),
      soaField("expire"),
      soaField("ttl", { label: "TTL" })
    ];
    return { columns };
  }
};
</script>
