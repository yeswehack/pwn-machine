<template>
  <BaseTable
    ref="table"
    name="router"
    rkey="name"
    :loading="loading"
    :data="routers"
    :columns="columns"
    v-on:delete="deleteRouter"
  >
    <template #body-cell-type="{row}">
      <TypeBadge :type="row.type" />
    </template>
    <template #body-cell-entrypoints="{row}">
      <div class="q-gutter-xs">
        <q-badge
          :key="idx"
          v-for="[idx, entrypoint] of (row.entryPoints || []).entries()"
        >
          {{ entrypoint }}
        </q-badge>
      </div>
    </template>
    <template #body-cell-service="{row}">
      <ServiceLink :name="row.service" />
    </template>
    <template #body-cell-middlewares="{row}">
      <MiddlewareLink
        :name="name"
        :key="idx"
        v-for="[idx, name] of (row.middlewares || []).entries()"
      />
    </template>
    <template #body-cell-status="{row}">
      <q-badge :color="statusColor(row.status)" class="q-ml-sm text-mono">
        {{ row.status == "enabled" ? "OK" : "ERROR" }}
      </q-badge>
    </template>

    <template #details="{ row }">
      <RouterDetails
        :name="row.name"
        :services="services"
        :routers="routers"
        :entrypoints="entrypoints"
        :middlewares="middlewares"
        v-on:modified="routerCreated"
        v-on:refetch="$emit('refetch')"
      />
    </template>
    <template #popup="{ info }">
      <CreateRouter
        :info="info"
        :services="services"
        :routers="routers"
        :entrypoints="entrypoints"
        popup
        v-on:created="routerCreated"
      />
    </template>
  </BaseTable>
</template>

<script>
import RouterDetails from "src/components/Traefik/Router/Details.vue";
import CreateRouter from "src/components/Traefik/Router/Create.vue";
import BaseTable from "src/components/BaseTable.vue";
import ServiceLink from "src/components/Traefik/Service/Link.vue";
import MiddlewareLink from "src/components/Traefik/Middleware/Link.vue";
import TypeBadge from "src/components/Traefik/TypeBadge.vue";

export default {
  // name: 'PageName',
  components: {
    CreateRouter,
    RouterDetails,
    BaseTable,
    ServiceLink,
    MiddlewareLink,
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
          label: "name",
          field: "name",
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "type",
          align: "left",
          label: "type",
          field: "type",
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "rule",
          label: "Rule",
          align: "left",
          field: "rule",
          sortable: true
        },
        {
          name: "entrypoints",
          label: "Entrypoints",
          align: "left",
          field: "entryPoints",
          format: val => val.join(""),
          sortable: true
        },
        {
          name: "service",
          label: "Service",
          align: "left",
          field: "service",
          sortable: true
        },
        {
          name: "middlewares",
          label: "Middlewares",
          align: "left",
          field: "middlewares",
          format: val => val.join(""),
          sortable: true
        },
        {
          name: "status",
          label: "Status",
          align: "left",
          field: "status",
          sortable: true
        }
      ]
    };
  },
  methods: {
    statusColor(status) {
      return status == "enabled" ? "positive" : "negative";
    },
    routerCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteRouter(name) {
      this.$api.docker.deleteRouter(name.split("@")[0]);
      this.$emit("refetch");
    }
  }
};
</script>
