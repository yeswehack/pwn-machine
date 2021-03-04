<template>
  <BaseTable
    ref="table"
    name="service"
    rkey="name"
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
          v-for="[idx, name] in (row.usedBy || []).entries()"
        />
      </div>
    </template>
    <template #body-cell-type="{row}">
      <TypeBadge :type="row.type" />
    </template>

    <template #body-cell-servers="{row}">
      <div class="q-gutter-xs">
        <q-badge
          :key="idx"
          :color="getServerStatusColor(row, server)"
          v-for="[idx, server] in getServers(row).entries()"
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
    <template #popup="{ info }">
      <CreateService
        popup
        :info="info"
        :services="services"
        :routers="routers"
        :entrypoints="entrypoints"
        v-on:created="serviceCreated"
      />
    </template>
  </BaseTable>
</template>

<script>
import ServiceDetails from "src/components/Traefik/Service/Details.vue";
import CreateService from "src/components/Traefik/Service/Create.vue";
import BaseTable from "src/components/BaseTable.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import TypeBadge from "src/components/Traefik/TypeBadge.vue";

export default {
  components: {
    CreateService,
    ServiceDetails,
    BaseTable,
    RouterLink,
    TypeBadge
  },
  props: {
    loading: Boolean,
    services: Array,
    routers: Array,
    entrypoints: Array,
    middlewares: Array
  },
  data() {
    return {
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "name",
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "type",
          align: "left",
          label: "Type",
          field: "type",
          sortable: true
        },
        {
          name: "usedBy",
          align: "left",
          label: "Connected routers",
          field: "usedBy",
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "servers",
          align: "left",
          label: "Servers",
          field: row => this.getServers(row),
          format: val => `${val.join()}`,
          sortable: true
        }
      ]
    };
  },
  methods: {
    getServerStatusColor(row, server) {
      if ("serverStatus" in row && server in row.serverStatus) {
        return row.serverStatus[server] == "UP" ? "positive" : "negative";
      }
      return "primary";
    },
    getServers(row) {
      if (!("loadBalancer" in row)) return [];
      const key = row.type == "http" ? "url" : "address";
      return row.loadBalancer.servers.map(s => s[key]);
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
