<template>
  <BaseTable
    ref="table"
    name="middleware"
    rkey="name"
    :data="middlewares"
    :columns="columns"
    v-on:delete="deleteMiddleware"
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

    <template #body-cell-enabled="{row}">
      <status-badge :status="row.enabled" />
    </template>
    <template #details="{ row }">
      <MiddlewareDetails
        :middlewares="middlewares"
        :name="row.name"
        v-on:modified="middlewareCreated"
      />
    </template>
    <template #popup="{ info }">
      <CreateMiddleware
        :info="info"
        popup
        :middlewares="middlewares"
        v-on:created="middlewareCreated"
      />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import MiddlewareDetails from "src/components/Traefik/Middleware/Details.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import Middleware from "src/components/Traefik/Middleware/Middleware.vue";
import db from "src/gql";
import StatusBadge from "src/components/Traefik/StatusBadge.vue";
export default {
  components: {
    CreateMiddleware,
    MiddlewareDetails,
    BaseTable,
    RouterLink,
    StatusBadge
  },
  apollo: {
    middlewares: {
      query: db.traefik.GET_MIDDLEWARES,
      update: data => data.traefikMiddlewares
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
      col("type"),
      { ...col("usedBy"), label: "Connected Routers" },
      { ...col("enabled"), label: "Status" }
    ];

    return {
      columns
    };
  },
  methods: {
    middlewareCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteMiddleware(name) {
      this.$api.docker.deleteMiddleware(name.split("@")[0]);
      this.$emit("refetch");
    }
  }
};
</script>
