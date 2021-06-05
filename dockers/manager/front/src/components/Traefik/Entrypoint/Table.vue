<template>
  <base-table
    ref="table"
    name="entrypoint"
    row-key="name"
    :query="$apollo.queries.entrypoints"
    :data="entrypoints"
    :columns="columns"
    no-details
    no-new
    no-menu
    @delete="deleteService"
  >
    <template #body-cell-protocol="{row}">
      <protocol-badge :protocol="row.protocol" />
    </template>
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-xs">
        <router-link
          :name="name"
          :key="idx"
          v-for="(name, idx) of row.usedBy.map(r => r.name)"
        />
      </div>
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import ProtocolBadge from "src/components/Traefik/ProtocolBadge.vue";
import api from "src/api";

export default {
  components: {
    BaseTable,
    ProtocolBadge,
    RouterLink
  },
  apollo: {
    entrypoints: {
      query: api.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    }
  },
  data() {
    const col = (name, opt = {}) => ({
      name: name,
      align: "left",
      label: name,
      field: name,
      autoWidth: true,
      sortable: true,
      ...opt
    });
    const columns = [
      col("protocol"),
      col("name", { autoWidth: false }),
      col("ipport", {
        autoWidth: false,
        label: "Listening on",
        classes: "text-mono",
        field: row => `${row.ip}:${row.port}`
      }),
      col("usedBy", { autoWidth: false })
    ];
    return { columns };
  },
  methods: {
    getServerStatusColor(row, server) {
      const serverStatus = row.serverStatus.find(({ url }) => url === server);
      if (serverStatus === undefined) {
        return "primary";
      }

      return serverStatus.status === "UP" ? "positive" : "negative";
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
