<template>
  <BaseTable
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
      <ProtocolBadge :protocol="row.protocol" />
    </template>
    <template #body-cell-entryPoints="{row}">
      <div class="q-gutter-xs">
        <q-badge :key="idx" v-for="(entrypoint, idx) of row.entryPoints">
          {{ entrypoint }}
        </q-badge>
      </div>
    </template>
    <template #body-cell-service="{row}">
      <ServiceLink :service="row.service" />
    </template>
    <template #body-cell-middlewares="{row}">
      <div class="q-gutter-xs">
        <MiddlewareLink
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
      <RouterDetails :router="row" />
    </template>
  </BaseTable>
</template>

<script>
import RouterDetails from "src/components/Traefik/Router/Details.vue";
import RouterDialog from "src/components/Traefik/Router/Dialog.vue";
import BaseTable from "src/components/BaseTable3.vue";
import ServiceLink from "src/components/Traefik/Service/Link.vue";
import MiddlewareLink from "src/components/Traefik/Middleware/Link.vue";
import ProtocolBadge from "src/components/Traefik/ProtocolBadge.vue";
import db from "src/gql";
import StatusBadge from "src/components/Traefik/StatusBadge.vue";

export default {
  components: {
    RouterDetails,
    BaseTable,
    ServiceLink,
    MiddlewareLink,
    ProtocolBadge,
    StatusBadge
  },
  apollo: {
    routers: {
      query: db.traefik.GET_ROUTERS,
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
        router
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
              mutation: db.traefik.DELETE_ROUTER,
              variables: { input },
              refetchQueries: [{ query: db.traefik.GET_ROUTERS }]
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
