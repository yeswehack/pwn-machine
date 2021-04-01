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
    <template #bottom>
      <div class="col">
        <q-select
          dense
          v-model="containerToConnect"
          :options="containersNotAlreadyConnected"
          label="Connect a container"
        >
          <template #after>
            
            <q-btn
              icon="eva-plus"
              round
              :disable="!containerToConnect"
              color="positive"
              size="sm"
              @click="attachContainer"
            />
          </template>
        </q-select>
      </div>
    </template>
    <template #no-data>
      <div class="col">
        <q-select
          dense
          v-model="containerToConnect"
          :options="containersNotAlreadyConnected"
          label="Connect a container"
        >
          <template #after>
            
            <q-btn
              icon="eva-plus"
              round
              :disable="!containerToConnect"
              color="positive"
              size="sm"
              @click="attachContainer"
            />
          </template>
        </q-select>
      </div>
    </template>
  </q-table>
</template>

<script>
import ContainerLink from "src/components/Docker/Container/Link.vue";
import graphql from "src/gql/docker";

const {
  mutations: {
    detachContainerFromDockerNetwork,
    attachContainerToDockerNetwork
  },
  queries: { getDockerContainers }
} = graphql;

export default {
  components: { ContainerLink },
  apollo: {
    containers: {
      query: getDockerContainers,
      update: data => data.docker.containers
    }
  },
  props: {
    network: Object
  },
  computed: {
    connected() {
      return this.network.connectedContainers;
    },
    containersNotAlreadyConnected() {
      return (this.containers || []).map(c => ({
        label: c.name,
        value: c.id,
        disable: !!this.connected.find(x => x.name == c.name)
      }));
    }
  },
  methods: {
    attachContainer() {
      this.runMutation(
        attachContainerToDockerNetwork,
        {
          network: this.network.name,
          container: this.containerToConnect.label
        },
        `Container ${this.containerToConnect.label} attached to ${this.network.name}.`,
        () => this.$emit("needRefresh")
      );
    },

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
    return { pagination, columns, containerToConnect: null };
  }
};
</script>

<style></style>
