<template>
  <base-table
    ref="table"
    name="middleware"
    row-key="name"
    :query="$apollo.queries.middlewares"
    :data="middlewares"
    :columns="columns"
    @create="createMiddleware"
    @clone="cloneMiddleware"
    @delete="deleteMiddleware"
  >
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-xs">
        <router-link
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
      <middleware-details :value="extraForm(row)"/>
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import MiddlewareDetails from "src/components/Traefik/Middleware/Details.vue";
import MiddlewareDialog from "src/components/Traefik/Middleware/Dialog.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import api from "src/api";
import StatusBadge from "src/components/Traefik/StatusBadge.vue";
export default {
  components: {
    MiddlewareDetails,
    BaseTable,
    RouterLink,
    StatusBadge
  },
  apollo: {
    middlewares: {
      query: api.traefik.middlewares.LIST_MIDDLEWARES,
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
      { ...col("usedBy"), label: "Used by" },
      { ...col("enabled"), label: "Status" }
    ];

    return {
      columns
    };
  },
  methods: {
    extraForm(f){
      return {...f, extra: f[f.type]} 
    },
    createMiddleware() {
      this.$q.dialog({
        component: MiddlewareDialog,
        parent: this
      });
    },
    cloneMiddleware(middleware) {
      this.$q.dialog({
        component: MiddlewareDialog,
        parent: this,
        middleware
      });
    },
    deleteMiddleware(middleware) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${middleware.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.$apollo
            .mutate({
              mutation: api.traefik.middlewares.DELETE_MIDDLEWARE,
              variables: { nodeId: middleware.nodeId },
              refetchQueries: [{ query: api.traefik.middlewares.LIST_MIDDLEWARES }]
            })
            .then(response => {
              const deleted = response.data.traefikDeleteMiddleware.ok;
              if (deleted) {
                this.$q.notify({
                  message: `${middleware.name} deleted.`,
                  type: "positive"
                });
              } else {
                this.$q.notify({
                  message: `Unable to delete ${middleware.name}.`,
                  type: "negative"
                });
              }
            });
        });
    }
  }
};
</script>
