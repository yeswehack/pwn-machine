<template>
  <base-grid-input
    :readonly="readonly"
    :titles="['Containers']"
    gridFormat="2fr 4fr 1fr"
    :entries="network.usedBy"
    @addEntry="connectContainer"
    @removeEntry="disconnectContainer"
  >
    <template #inputs>
      <q-select
        label="Container name"
        :loading="loading"
        :options="containersNotAlreadyConnected"
        @input="fillAliases"
        v-model="model.container"
      />
      <q-select
        label="Aliases"
        use-input
        use-chips
        multiple
        new-value-mode="add"
        :loading="loading"
        hide-dropdown-icon
        v-model="model.aliases"
        style="grid-column-start:2;grid-column-end:4;"
      />
    </template>
    <template #entry="{entry}">
      <div class="ellipsis">
        <container-link :name="entry.container.name" class="q-mr-md" />
      </div>
      <div class="ellipsis">
        {{ entry.aliases ? entry.aliases.join(", ") : "-" }}
      </div>
      <div class="ellipsis text-right">
        {{ entry.ipAddress || "Off-line" }}
      </div>
    </template>
  </base-grid-input>
</template>

<script>
import api from "src/api";
import BaseGridInput from "src/components/BaseGridInput.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import { notify } from "src/utils";
export default {
  components: { BaseGridInput, ContainerLink },
  props: {
    readonly: { type: Boolean, default: false },
    network: { type: Object, default: null },
    container: { type: Object, default: null }
  },
  data() {
    return { model: { container: null, aliases: [] }, loading: false };
  },
  apollo: {
    containers: {
      query: api.docker.containers.LIST_CONTAINERS,
      update: data => data.dockerContainers
    }
  },
  computed: {
    containersNotAlreadyConnected() {
      return (this.containers || [])
        .filter(c => !this.network.usedBy.some(f => f.containerName == c.name))
        .map(c => ({
          label: c.name,
          value: c
        }));
    }
  },
  methods: {
    fillAliases({ value: container }) {
      const aliases = [container.name];

      const serviceName = container.labels.find(
        l => l.key == "com.docker.compose.service"
      )?.value;
      if (serviceName && serviceName != container.name) {
        aliases.push(serviceName);
      }
      this.model.aliases = aliases;
    },
    connectContainer() {
      const containerId = this.model.container.value.id;
      const aliases = this.model.aliases;
      const input = { networkId: this.network.id, containerId, aliases };
      this.mutate({
        mutation: api.docker.networks.CONNECT_TO_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }],
        message: `${this.model.container.value.name} connected to ${this.network.name}`
      }).finally(() => {
        this.model.container = null;
        this.model.aliases = [];
      });
    },
    disconnectContainer(id) {
      const container = this.network.usedBy[id].container;
      const input = { networkId: this.network.id, containerId: container.id };
      this.mutate({
        mutation: api.docker.networks.DISCONNECT_FROM_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }],
        message: `${container.name} disconnected from ${this.network.name}`
      });
    }
  }
};
</script>
