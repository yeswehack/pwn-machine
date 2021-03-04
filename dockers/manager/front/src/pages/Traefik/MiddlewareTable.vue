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
        <router-link
          :to="{ path: `/traefik/routers`, hash: router }"
          :key="idx"
          v-for="[idx, router] in (row.usedBy || []).entries()"
        >
          <q-badge>{{ router }}</q-badge>
        </router-link>
      </div>
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
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import Middleware from "src/components/Traefik/Middleware/Middleware.vue";

export default {
  components: { CreateMiddleware, MiddlewareDetails, BaseTable },
  props: {
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
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "usedBy",
          align: "left",
          label: "Connected routers",
          field: "usedBy",
          format: val => `${val}`,
          sortable: true
        }
      ]
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
