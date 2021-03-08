<template>
  <BaseTable
    ref="table"
    name="zone"
    :loading="$apollo.loading"
    :data="zones"
    :columns="columns"
    @deleteRow="deleteZone"
  >
    <template v-slot:details="{ row }">
      <ZoneDetails :zone="row" />
    </template>
    <template v-slot:popup="{ row, closePopup }">
      <CreateZone :value="row" @close="closePopup" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable2.vue";
import CreateZone from "src/components/DNS/Zone/Create.vue";
import ZoneDetails from "src/components/DNS/Zone/Details.vue";

import graphql from "src/gql/dns";
const {
  mutations: { deleteDnsZone },
  queries: { getDnsZones }
} = graphql;

export default {
  components: { BaseTable, CreateZone, ZoneDetails },
  apollo: {
    zones: {
      query: getDnsZones,
      update: data => data.dns.zones
    }
  },
  created() {
    this.$root.$on("refresh", () => this.$apollo.queries.zones.refetch());
  },
  methods: {
    deleteZone(zone) {
      const variables = {
        zone: zone.name
      };
      this.runMutation(
        deleteDnsZone,
        variables,
        `Zone ${zone.name} deleted.`,
        store => {
          const data = store.readQuery({ query: getDnsZones });
          data.dns.zones = data.dns.zones.filter(z => z.id != zone["id"]);
          store.writeQuery({ query: getDnsZones, data });
        }
      );
    },
    refresh() {
      this.$apollo.queries.zones.refetch();
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
