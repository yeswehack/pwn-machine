<template>
  <base-grid-input
    :readonly="readonly"
    :titles="['Containers']"
    gridFormat="2fr 4fr 1fr"
    :entries="container.connections"
    @addEntry="connectNetwork"
    @removeEntry="disconnectNetwork"
  >
    <template #inputs>
      <q-select
        label="Network name"
        :loading="loading"
        :options="networksNotAlreadyConnected"
        v-model="model.network"
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
        <network-link :name="entry.network.name" class="q-mr-md" />
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
import NetworkLink from "src/components/Docker/Network/Link.vue";
import { notify } from "src/utils";
export default {
  components: { BaseGridInput, NetworkLink },
  props: {
    readonly: { type: Boolean, default: false },
    network: { type: Object, default: null },
    container: { type: Object, default: null }
  },
  data() {
    const defaultAliases = [this.container.name];

    const serviceName = this.container.labels.find(
      l => l.key == "com.docker.compose.service"
    )?.value;
    if (serviceName && serviceName != this.container.name) {
      defaultAliases.push(serviceName);
    }
    return { model: { network: null, aliases: defaultAliases }, defaultAliases,  loading: false };
  },
  apollo: {
    networks: {
      query: api.docker.networks.LIST_NETWORKS,
      update: data => data.dockerNetworks
    }
  },
  computed: {
    networksNotAlreadyConnected() {
      return (this.networks || [])
        .filter(
          n => !this.container.connections.some(c => c.network.name == n.name)
        )
        .map(c => ({
          label: c.name,
          value: c
        }));
    }
  },
  methods: {
    connectNetwork() {
      const networkId = this.model.network.value.id;
      const aliases = this.model.aliases;
      const input = { containerId: this.container.id, networkId, aliases };
      this.$apollo
        .mutate({
          mutation: api.docker.networks.CONNECT_TO_NETWORK,
          variables: { input },
          refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
        })
        .then(
          notify(
            `${this.container.name} connected to ${this.model.network.value.name}`
          )
        )
        .then(() => {
          this.model.network = null;
          this.model.aliases = this.defaultAliases;
        });
    },
    disconnectNetwork(id) {
      const network = this.container.connections[id].network
      const input = { networkId: network.id, containerId: this.container.id };
      this.$apollo
        .mutate({
          mutation: api.docker.networks.DISCONNECT_FROM_NETWORK,
          variables: { input },
          refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
        })
        .then(
          notify(`${this.container.name} disconnected from ${network.name}`)
        );
    }
  }
};
</script>
