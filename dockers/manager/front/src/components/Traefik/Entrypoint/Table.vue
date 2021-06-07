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
};
</script>
