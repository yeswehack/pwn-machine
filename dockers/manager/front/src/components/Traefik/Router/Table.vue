<template>
  <base-table
    ref="table"
    name="router"
    row-key="name"
    :query="$apollo.queries.routers"
    :data="routers"
    :columns="columns"
    @create="createRouter"
    @delete="deleteRouter"
    @clone="cloneRouter"
  >
    <template #body-cell-type="{row}">
      <protocol-badge :protocol="row.protocol" />
    </template>
    <template #body-cell-entryPoints="{row}">
      <div class="q-gutter-xs">
        <entrypoint-link
          :name="entrypoint.name"
          :key="idx"
          v-for="(entrypoint, idx) of row.entryPoints"
        />
      </div>
    </template>
    <template #body-cell-service="{row}">
      <service-link :service="row.service" />
    </template>
    <template #body-cell-middlewares="{row}">
      <div class="q-gutter-xs">
        <middleware-link
          :name="middleware.name"
          :key="idx"
          v-for="(middleware, idx) of row.middlewares"
        />
      </div>
    </template>
    <template #body-cell-enabled="{row}">
      <status-badge :status="row.enabled" />
    </template>

    <template #details="{ row }">
      <router-details :value="extraForm(row)" />
    </template>
  </base-table>
</template>

<script>
import RouterDetails from "src/components/Traefik/Router/Details.vue";
import RouterDialog from "src/components/Traefik/Router/Dialog.vue";
import BaseTable from "src/components/BaseTable.vue";
import ServiceLink from "src/components/Traefik/Service/Link.vue";
import EntrypointLink from "src/components/Traefik/Entrypoint/Link.vue";
import MiddlewareLink from "src/components/Traefik/Middleware/Link.vue";
import ProtocolBadge from "src/components/Traefik/ProtocolBadge.vue";
import api from "src/api";
import StatusBadge from "src/components/Traefik/StatusBadge.vue";

export default {
  components: {
    RouterDetails,
    EntrypointLink,
    BaseTable,
    ServiceLink,
    MiddlewareLink,
    ProtocolBadge,
    StatusBadge
  },
  apollo: {
    routers: {
      query: api.traefik.routers.LIST_ROUTERS,
      update: data => data.traefikRouters
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
      col("rule"),
      col("entryPoints"),
      col("middlewares"),
      col("service"),
      col("enabled")
    ];

    return {
      columns
    };
  },
  methods: {
    extraForm(f) {
      const extra = {
        rule: f.rule,
        priority: f.priority,
        entryPoints: (f.entryPoints ?? []).map(ep => ep.name),
        service: f.service?.name,
        middlewares: (f.middlewares ?? []).map(m => m.name)
      };

      return { ...f, extra };
    },
    createRouter() {
      this.$q.dialog({
        component: RouterDialog,
        parent: this
      });
    },
    cloneRouter(router) {
      this.$q.dialog({
        component: RouterDialog,
        parent: this,
        router: this.extraForm(router)
      });
    },
    routerCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteRouter(router) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${router.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.$apollo
            .mutate({
              mutation: api.traefik.routers.DELETE_ROUTER,
              variables: { id: router.nodeId },
              refetchQueries: [{ query: api.traefik.routers.LIST_ROUTERS }]
            })
            .then(response => {
              this.$q.notify({
                message: `${router.name} deleted.`,
                type: "positive"
              });
            })
            .catch(e => {
              this.$q.notify({
                message: `${e.message}`,
                type: "negative"
              });
            });
        });
    }
  }
};
</script>
