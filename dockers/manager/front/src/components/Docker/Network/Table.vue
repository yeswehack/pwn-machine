<template>
  <base-table
    ref="table"
    name="network"
    row-key="name"
    :loading="$apollo.loading"
    :data="networks"
    :columns="columns"
    @create="createNetwork"
    @clone="cloneNetwork"
    @delete="deleteNetwork"
  >
    <template #body-cell-name="{value, row}">
      <span
        style="text-decoration:underline;text-decoration-style:dotted"
        v-if="row.builtin"
      >
        {{ value }}
        <q-tooltip anchor="center right" self="center left">Built-in</q-tooltip>
      </span>
      <span v-else>
        {{ value }}
      </span>
    </template>

    <template #body-cell-internal="{value}">
      <q-badge color="positive" label="yes" v-if="value" />
      <q-badge color="negative" label="no" v-else />
    </template>

    <template #body-cell-containers="{row}">
      <div class="row q-gutter-sm">
        <container-link
          :name="connection.container.name"
          :key="idx"
          v-for="(connection, idx) of row.connections"
        >
          <q-tooltip
            v-if="row.name == 'host'"
            anchor="top middle"
            self="bottom middle"
          >
            Host
          </q-tooltip>
          <q-tooltip
            v-else-if="connection.ipv4Address || connection.ipv6Address"
            anchor="top middle"
            self="bottom middle"
          >
            {{ connection.ipv4Address }} {{ connection.ipv6Address }}
          </q-tooltip>
        </container-link>
      </div>
    </template>

    <template #details="{ row }">
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
  components: {
    BaseTable,
    NetworkDetails,
    ContainerLink
  },
  apollo: {
    networks: {
      query: api.docker.GET_NETWORKS,
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
      col("internal"),
      col("gateway", {
        classes: "text-mono",
        field: ({ ipams }) => ipams[0]?.gateway
      }),
      col("subnet", {
        classes: "text-mono",
        field: ({ ipams }) => ipams[0]?.subnet
      }),
      col("containers", { label: "Connected containers" })
    ];
    return { columns };
  },
  methods: {
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
        .onOk(() => {});
    }
  }
};
</script>
