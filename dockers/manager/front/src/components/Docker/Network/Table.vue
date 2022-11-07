<template>
  <base-table
    ref="table"
    name="network"
    row-key="name"
    :query="$apollo.queries.networks"
    :data="networks"
    :columns="columns"
    @create="createNetwork"
    @clone="cloneNetwork"
    @delete="deleteNetwork"
  >
    <template #header-button>
      <q-btn
        rounded
        label="Prune"
        color="negative"
        icon="eva-trash-outline"
        @click="pruneNetworks"
      />
    </template>
    <template #body-cell-name="{value, row}">
      <span
        v-if="row.builtin"
        style="text-decoration:underline;text-decoration-style:dotted"
      >
        {{ value }}
        <q-tooltip anchor="center right" self="center left">Built-in</q-tooltip>
      </span>
      <span v-else>
        {{ value }}
      </span>
    </template>

    <template #body-cell-internal="{value}">
      <q-badge v-if="value" color="positive" label="yes" />
      <q-badge v-else color="negative" label="no" />
    </template>

    <template #body-cell-usedBy="{row}">
      <div class="row q-gutter-sm">
        <container-link
          v-for="(connection, idx) of row.usedBy"
          :key="idx"
          :name="connection.container.name"
        >
          <q-tooltip
            v-if="row.name === 'host'"
            anchor="top middle"
            self="bottom middle"
          >
            Host
          </q-tooltip>
          <q-tooltip
            v-else-if="connection.ipAddress"
            anchor="top middle"
            self="bottom middle"
          >
            {{ connection.ipv4Address }} {{ connection.ipAddress }}
          </q-tooltip>
        </container-link>
      </div>
    </template>

    <template #details="{row}">
      <network-details :network="row" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import NetworkDialog from "src/components/Docker/Network/Dialog.vue";
import NetworkDetails from "src/components/Docker/Network/Details.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";

export default {
  components: { BaseTable, NetworkDetails, ContainerLink },
  apollo: {
    networks: {
      query: api.docker.networks.LIST_NETWORKS,
      update: ({ dockerNetworks }) => dockerNetworks
    }
  },
  data() {
    const col = (name, opts = {}) => ({
      name,
      align: "left",
      label: name,
      field: name,
      sortable: true,
      ...opts
    });
    const columns = [
      col("name"),
      col("internal", { autoWidth: true }),
      col("gateway", {
        classes: "text-mono",
        field: ({ ipams }) => ipams[0]?.gateway
      }),
      col("subnet", {
        classes: "text-mono",
        field: ({ ipams }) => ipams[0]?.subnet
      }),
      col("usedBy", { label: "Connected containers" })
    ];
    return { columns };
  },
  methods: {
    pruneNetworks() {
      this.$q
        .dialog({
          title: "Prune networks ?",
          message:
            "This will remove all networks not used by at least one container.",
          color: "negative",
          type: "confirm",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.networks.PRUNE_NETWORKS,
            refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }]
          }).then(result => {
            const deleted = result.deleted;
            const message = deleted.length
              ? `${deleted.length} network(s) deleted: ${deleted.join(", ")}`
              : `No network deleted.`;
            this.$q.notify({
              message,
              type: "positive"
            });
          });
        });
    },
    getDriverColor(driver) {
      switch (driver) {
        case "host":
          return "positive";
        case "bridge":
          return "primary";
        case "null":
          return "negative";
      }
      return "orange";
    },
    createNetwork() {
      this.$q.dialog({
        component: NetworkDialog,
        parent: this
      });
    },
    cloneNetwork(network) {
      this.$q.dialog({
        component: NetworkDialog,
        parent: this,
        network
      });
    },
    deleteNetwork(network) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${network.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.networks.DELETE_NETWORK,
            variables: { id: network.id },
            refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }],
            message: `${network.name} deleted.`
          });
        });
    }
  }
};
</script>
