<template>
  <base-table
    ref="table"
    name="router"
    row-key="name"
    @create="createRouter"
    @delete="deleteRouter"
    @clone="cloneRouter"
    :loading="$apollo.queries.routers.loading"
    :data="routers"
    :columns="columns"
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
      <router-details :router="extraForm(row)" />
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
      query: api.traefik.GET_ROUTERS,
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
      return { ...f, extra: f[f.protocol] };
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
          const input = { protocol: router.protocol, name: router.name };
          this.$apollo
            .mutate({
              mutation: api.traefik.DELETE_ROUTER,
              variables: { input },
              refetchQueries: [{ query: api.traefik.GET_ROUTERS }]
            })
            .then(response => {
              const deleted = response.data.traefikDeleteRouter.ok;
              if (deleted) {
                this.$q.notify({
                  message: `${router.name} deleted.`,
                  type: "positive"
                });
              } else {
                this.$q.notify({
                  message: `Unable to delete ${router.name}.`,
                  type: "negative"
                });
              }
            });
        });
    }
  }
};
</script>
