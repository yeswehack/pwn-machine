<template>
  <BaseTable
    ref="table"
    name="network"
    rkey="name"
    :loading="loading"
    :data="networks"
    :columns="columns"
    @deleteRow="deleteNetwork"
  >
    <template #body-cell-driver="{row}">
      <q-badge :color="getDriverColor(row.driver)" :label="row.driver" />
    </template>

    <template #body-cell-internal="{value}">
      <q-badge color="positive" label="yes" v-if="value" />
      <q-badge color="negative" label="no" v-else />
    </template>

    <template #body-cell-containers="{row: {usedBy}}">
      <div class="q-gutter-sm row">
        <ContainerLink :name="name" :key="name" v-for="{ name } of usedBy" />
      </div>
    </template>

    <!--template #details="{ row }">
      <NetworkDetails :name="row.name" />
    </template-->

    <template #popup="{ row, closePopup }">
      <CreateNetwork :value="row" @close="closePopup" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import CreateNetwork from "src/components/Docker/Network/Create.vue";
import NetworkDetails from "src/components/Docker/Network/Details.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import gql from "src/gql";

export default {
  components: {
    BaseTable,
    CreateNetwork,
    //NetworkDetails,
    ContainerLink
  },
  apollo: {
    networks: {
      query: gql.docker.GET_NETWORKS,
      update: ({ dockerNetworks }) => dockerNetworks
    }
  },
  created() {
    this.$root.$on("refresh", () => this.$apollo.queries.networks.refetch());
  },
  computed: {
    loading() {
      return this.$apollo.queries.networks.loading;
    }
  },
  data() {
    const field = (n, opt = {}) => ({
      name: n,
      align: "left",
      label: n,
      field: n,
      sortable: true,
      ...opt
    });
    const columns = [
      field("name"),
      field("driver"),
      field("internal"),
      field("gateway", { classes: "text-mono" }),
      field("subnet", { classes: "text-mono" }),
      field("containers", {
        label: "Connected containers",
        field: row => row.usedBy.map(c => c.name)
      })
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
    deleteNetwork(network) {
      const variables = {
        name: network.name
      };

      this.runMutation(
        gql.docker.DELETE_NETWORK,
        variables,
        `Network ${network.name} deleted.`,
        store => {
          const data = store.readQuery({ query: gql.docker.GET_NETWORKS });
          data.docker.networks = data.docker.networks.filter(
            n => n.id != network.id
          );
          store.writeQuery({ query: gql.docker.GET_NETWORKS, data });
        }
      );
    }
  }
};
</script>
