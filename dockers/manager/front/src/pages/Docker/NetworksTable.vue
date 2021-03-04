<template>
  <BaseTable
    ref="table"
    name="network"
    rkey="Name"
    :loading="loading"
    :data="networks"
    :columns="columns"
    v-on:delete="deleteContainer"
  >
    <template #body-cell-driver="{row}">
      <!-- <q-badge :color="getDriverColor(row.Driver)"> -->
      {{ row.Driver }}
      <!-- </q-badge> -->
    </template>

    <template #body-cell-internal="{row}">
      <q-badge color="negative" label="internal" v-if="row.Internal" />
    </template>

    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row">
        <ContainerLink
          :name="container.Name"
          :key="name"
          v-for="[name, container] of Object.entries(row.Containers)"
        />
      </div>
    </template>

    <template #popup="{ info }">
      <CreateNetwork :info="info" v-on:created="networkCreated" />
    </template>

    <template #details="{ row }">
      <NetworkDetails :network="row" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import CreateNetwork from "src/components/Docker/Network/Create.vue";
import NetworkDetails from "src/components/Docker/Network/Details.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import { mapGetters } from "vuex";
export default {
  components: { BaseTable, CreateNetwork, NetworkDetails, ContainerLink },
  props: {
    containers: Array,
    networks: Array,
    volumes: Array
  },
  computed: mapGetters(["loading"]),
  data() {
    return {
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "Name",
          sortable: true
        },
        {
          name: "driver",
          label: "Driver",
          align: "left",
          field: "Driver",
          sortable: true
        },
        {
          name: "internal",
          label: "Internal",
          align: "left",
          field: row => {
            return row.Internal ? "internal" : "external";
          },
          sortable: true
        },
        {
          name: "fateway",
          label: "Gateway",
          align: "left",
          style: "font-family: monospace",
          field: row => {
            return this.getGateway(row);
          },
          sortable: true
        },
        {
          name: "subnet",
          label: "Subnet",
          align: "left",
          style: "font-family: monospace",
          field: row => {
            return this.getSubnet(row);
          },
          sortable: true
        },
        {
          name: "containers",
          label: "Connected containers",
          align: "left",
          field: row => Object.values(row.Containers).map(r => r.Name),
          sortable: true
        }
      ]
    };
  },
  methods: {
    getGateway(network) {
      if (network.Driver != "bridge") {
        return "n/a";
      }
      return network.IPAM.Config.find(conf => "Gateway" in conf).Gateway;
    },
    getSubnet(network) {
      if (network.Driver != "bridge") {
        return "n/a";
      }
      return network.IPAM.Config.find(conf => "Subnet" in conf).Subnet;
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
    networkCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteContainer(name) {
      this.$api.docker.deleteContainer(name.split("@")[0]);
      this.$emit("refetch");
    }
  }
};
</script>
