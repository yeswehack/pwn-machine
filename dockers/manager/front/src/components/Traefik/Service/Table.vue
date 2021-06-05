<template>
  <base-table
    class=""
    ref="table"
    name="service"
    row-key="name"
    :query="$apollo.queries.services"
    :data="services"
    :columns="columns"
    @create="createService"
    @clone="cloneService"
    @delete="deleteService"
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
    <template #body-cell-protocol="{row}">
      <protocol-badge :protocol="row.protocol" />
    </template>

    <template #body-cell-enabled="{row}">
      <status-badge :status="row.enabled" />
    </template>
    <template #details="{ row }">
      <service-details :value="extraForm(row)" />
    </template>
  </base-table>
</template>

<script>
import ServiceDetails from "src/components/Traefik/Service/Details.vue";
import ServiceDialog from "src/components/Traefik/Service/Dialog.vue";
import BaseTable from "src/components/BaseTable.vue";
import RouterLink from "src/components/Traefik/Router/Link.vue";
import ProtocolBadge from "src/components/Traefik/ProtocolBadge.vue";
import api from "src/api";
import StatusBadge from "src/components/Traefik/StatusBadge.vue";

export default {
  components: {
    ServiceDetails,
    BaseTable,
    RouterLink,
    ProtocolBadge,
    StatusBadge
  },
  apollo: {
    services: {
      query: api.traefik.services.LIST_SERVICES,
      update: data => data.traefikServices
    }
  },
  data() {
    const col = (name, x = {}) => ({
      name,
      align: "left",
      field: name,
      label: name,
      sortable: true,
      autoWidth: true,
      ...x
    });
    const columns = [
      col("name"),
      col("protocol"),
      col("type"),
      col("usedBy", { label: "Connected Routers", autoWidth: false }),
      col("enabled", { label: "Status" })
    ];
    return { columns };
  },
  methods: {
    extraForm(f) {
      return { ...f, extra: f[f.type] };
    },
    createService() {
      this.$q.dialog({
        component: ServiceDialog,
        parent: this
      });
    },
    cloneService(service) {
      this.$q.dialog({
        component: ServiceDialog,
        parent: this,
        service
      });
    },
    deleteService(service) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${service.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.traefik.services.DELETE_SERVICE,
            variables: { nodeId: service.nodeId },
            refetchQueries: [{ query: api.traefik.services.LIST_SERVICES }],
            message: `${service.name} deleted.`
          });
        });
    }
  }
};
</script>
