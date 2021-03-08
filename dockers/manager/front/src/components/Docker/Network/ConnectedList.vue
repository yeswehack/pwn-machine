<template>
  <q-table
    title="Connected containers"
    dense
    :pagination="pagination"
    hide-pagination
    :data="connected"
    :columns="columns"
    row-key="name"
    no-data-label="No container connected"
  >
    <template #bottom>
      <div
        class="col col-12 row justify-center cursor-pointer"
        @click="attachContainer"
      >
        <div class="q-py-sm col col-auto">
          <q-btn flat size="xs" class="bg-positive" rounded icon="eva-plus" />
        </div>
      </div>
    </template>
    <template #body-cell-name="props">
      <q-td> <ContainerLink :name="props.value" /> </q-td>
    </template>
    <template #body-cell-detach="{row}">
      <q-td key="detach" auto-width class="cursor-pointer">
        <q-btn
          title="Detach container"
          icon="eva-close"
          round
          size="xs"
          @click="detachContainer(row.name)"
          color="negative"
        />
      </q-td>
    </template>
  </q-table>
</template>

<script>
import ContainerLink from "src/components/Docker/Container/Link.vue";
import graphql from "src/gql/docker";

const {
  mutations: { detachContainerFromDockerNetwork },
  queries: { getDockerNetworks }
} = graphql;

export default {
  components: { ContainerLink },
  props: {
    network: Object
  },
  computed: {
    connected() {
      return this.network.connectedContainers;
    }
  },
  methods: {
    attachContainer() {},
    detachContainer(n) {
      this.runMutation(
        detachContainerFromDockerNetwork,
        {
          network: this.network.name,
          container: n
        },
        `Container ${n} detached from ${this.network.name}.`,
        () => this.$emit("needRefresh")
      );
    }
  },
  data() {
    const pagination = {
      rowsPerPage: 0,
      sortBy: "ip"
    };
    const columns = [
      {
        name: "name",
        align: "left",
        label: "Name",
        field: "name",
        sortable: true
      },
      {
        name: "ip",
        label: "IP",
        field: row => [row.ipv4, row.ipv6].filter(x => x).join(", "),
        format: val => val,
        sortable: true
      },
      {
        name: "detach",
        align: "left",
        label: "",
        field: "",
        sortable: true
      }
    ];
    return { pagination, columns };
  }
};
</script>

<style></style>
