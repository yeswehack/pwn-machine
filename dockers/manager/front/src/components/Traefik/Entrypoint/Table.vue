<template>
  <base-table
    ref="table"
    name="entrypoint"
    row-key="name"
    :loading="$apollo.queries.entrypoints.loading"
    :data="entrypoints"
    :columns="columns"
    v-on:delete="deleteService"
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
    <template #details>
      <div>details</div>
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
      {
        ...col("ipport"),
        label: "Listening on",
        classes: "text-mono",
        field: row => `${row.ip}:${row.port}`
      },
      col("usedBy")
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
