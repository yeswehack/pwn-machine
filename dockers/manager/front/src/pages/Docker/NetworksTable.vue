<template>
  <BaseTable
    ref="table"
    name="network"
    rkey="name"
    :loading="loading"
    :data="networks"
    :columns="columns"
    v-on:delete="deleteContainer"
  >
    <template #body-cell-driver="{row}">
      <q-badge :color="getDriverColor(row.driver)" :label="row.driver"/>
    </template>

    <template #body-cell-internal="{row}">
      <q-badge color="negative" label="internal" v-if="row.internal" />
    </template>

    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row">
        <ContainerLink
          :name="name"
          :key="name"
          v-for="{ name } of row.usedBy"
        />
      </div>
    </template>

    <template #popup="{ info }">
      <CreateNetwork :info="info" v-on:created="networkCreated" />
    </template>

    <template #details="{ row }">
      <NetworkDetails :name="row.name" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import CreateNetwork from "src/components/Docker/Network/Create.vue";
import NetworkDetails from "src/components/Docker/Network/Details.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import { mapGetters } from "vuex";

import gql from "graphql-tag";

export default {
  components: { BaseTable, CreateNetwork, NetworkDetails, ContainerLink },
  apollo: {
    networks: {
      query: gql`
        query {
          docker {
            networks {
              name
              driver
              internal
              gateway
              subnet
              usedBy {
                id
                name
              }
            }
          }
        }
      `,
      update: data => data.docker.networks
    }
  },
  computed: {
    loading(){
      return this.$apollo.queries.networks.loading
    }
  },
  data() {
    return {
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "name",
          sortable: true
        },
        {
          name: "driver",
          label: "Driver",
          align: "left",
          field: "driver",
          sortable: true
        },
        {
          name: "internal",
          label: "internal",
          align: "left",
          field: "internal",
          format: row => (row.Internal ? "internal" : "external"),
          sortable: true
        },
        {
          name: "gateway",
          label: "Gateway",
          align: "left",
          style: "font-family: monospace",
          field: "gateway",
          sortable: true
        },
        {
          name: "subnet",
          label: "Subnet",
          align: "left",
          style: "font-family: monospace",
          field: "subnet",
          sortable: true
        },
        {
          name: "containers",
          label: "Connected containers",
          align: "left",
          field: row => row.usedBy.map(c => c.name),
          sortable: true
        }
      ]
    };
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
