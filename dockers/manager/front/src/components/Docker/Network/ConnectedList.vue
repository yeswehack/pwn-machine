<template>
  <q-table
  flat
    title="Connected containers"
    :pagination="pagination"
    hide-pagination
    :data="connected"
    :columns="columns"
    row-key="name"
    no-data-label="No container connected"
  >
    <template #body-cell-name="props">
      <q-td> <container-link :name="props.value" /> </q-td>
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
import api from "src/api";

export default {
  components: { ContainerLink },
  apollo: {
    containers: {
      query: api.docker.GET_CONTAINERS,
      update: data => data.dockerContainers
    }
  },
  props: {
    network: { type: Object, default: null }
  },
  computed: {
    connected() {
      return this.network.containers;
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
        gql.docker.ATTACH_CONTAINER_TO_NETWORK,
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
        gql.docker.DETACH_CONTAINER_FROM_NETWORK,
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
