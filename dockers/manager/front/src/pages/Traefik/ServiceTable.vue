<template>
  <BaseTable
    ref="table"
    name="service"
    row-key="name"
    :loading="loading"
    :data="services"
    :columns="columns"
    v-on:delete="deleteService"
  >
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-xs">
        <RouterLink
          :name="name"
          :key="idx"
          v-for="(name, idx) of row.usedBy.map(r => r.name)"
        />
      </div>
    </template>
    <template #body-cell-protocol="{row}">
      <ProtocolBadge :protocol="row.protocol" />
    </template>

    <template #body-cell-servers="{row}">
      <div class="q-gutter-xs">
        <q-badge
          :key="idx"
          :color="getServerStatusColor(row, server)"
          v-for="(server, idx) of getServers(row)"
          :label="server"
        />
      </div>
    </template>

    <template #details="{ row }">
      <ServiceDetails
        :name="row.name"
        :services="services"
        :routers="routers"
        :entrypoints="entrypoints"
        v-on:modified="serviceCreated"
      />
    </template>
  </BaseTable>
</template>

<script>
import ServiceDetails from "src/components/Traefik/Service/Details.vue";
import CreateService from "src/components/Traefik/Service/Create.vue";
import BaseTable from "src/components/BaseTable3.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import ProtocolBadge from "src/components/Traefik/ProtocolBadge.vue";
import db from "src/gql";

export default {
  components: {
    ServiceDetails,
    BaseTable,
    RouterLink,
    ProtocolBadge
  },
  props: {
    loading: Boolean,
    routers: Array,
    entrypoints: Array,
    middlewares: Array
  },
  apollo: {
    services: {
      query: db.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
  },
  data() {
    const col = name => ({
      name,
      align: "left",
      field: name,
      label: name,
      sortable: true
    });
    const columns = [
      col("name"),
      col("protocol"),
      { ...col("usedBy"), label: "Connected Routers" },
      col("servers")
    ];

    return {
      columns
    };
  },
  methods: {
    getServerStatusColor(row, server) {
      const serverStatus = row.serverStatus.find(({ url }) => url === server);
      if (serverStatus === undefined) {
        return "primary";
      }

      return serverStatus.status == "UP" ? "positive" : "negative";
    },
    getServers(row) {
      return row.loadBalancer?.servers.map(s => s.url) || [];
    },
    serviceCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteService(name) {
      this.$api.docker.deleteService(name.split("@")[0]);
      this.$emit("refetch");
    }
  }
};
</script>
