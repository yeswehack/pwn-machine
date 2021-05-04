<template>
  <base-table
    ref="table"
    name="zone"
    row-key="nodeId"
    :loading="$apollo.queries.zones.loading"
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
import BaseTable from "src/components/BaseTable3.vue";
import ZoneDialog from "src/components/DNS/Zone/Dialog.vue";
import ZoneDetails from "src/components/DNS/Zone/Details.vue";

import db from "src/gql/";

export default {
  components: { BaseTable, ZoneDetails },
  apollo: {
    zones: {
      query: db.dns.GET_ZONES,
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
          this.$apollo.mutate({
            mutation: db.dns.DELETE_ZONE,
            variables: { nodeId: zone.nodeId },
            refetchQueries: [
              { query: db.dns.GET_ZONES },
              { query: db.dns.GET_RULES }
            ]
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
      ...opt
    });

    const soaField = (name, opt = {}) =>
      field(name, { field: r => r.soa[name], ...opt });
    const columns = [
      field("name"),
      soaField("nameserver"),
      soaField("postmaster"),
      field("serial"),
      soaField("refresh"),
      soaField("retry"),
      soaField("expire"),
      soaField("ttl", { label: "TTL" })
    ];

    return {
      columns
    };
  }
};
</script>

<style></style>
