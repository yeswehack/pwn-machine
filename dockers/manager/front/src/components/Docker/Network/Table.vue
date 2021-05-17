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
    <template #body-cell-driver="{row}">
      <q-badge :color="getDriverColor(row.driver)" :label="row.driver" />
    </template>

    <template #body-cell-internal="{value}">
      <q-badge color="positive" label="yes" v-if="value" />
      <q-badge color="negative" label="no" v-else />
    </template>

    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row">
        <container-link
          :name="name"
          :key="name"
          v-for="{ name } of row.usingContainers"
        />
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
import gql from "src/gql";

export default {
  components: {
    BaseTable,
    NetworkDetails,
    ContainerLink
  },
  apollo: {
    networks: {
      query: gql.docker.GET_NETWORKS,
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
      col("driver"),
      col("internal"),
      col("gateway", { classes: "text-mono" }),
      col("subnet", { classes: "text-mono" }),
      col("containers", { label: "used by" })
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
