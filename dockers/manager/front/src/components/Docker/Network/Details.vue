<template>
  <div class="row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <create-network :value="network" readonly />
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section>
          <container-list-input
            @add="connectContainer"
            @remove="disconnectContainer"
            :value="network.usedBy.map(c=>c.container)"
            title="Connected containers"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import CreateNetwork from "./Create.vue";
import ContainerListInput from "../ContainerListInput.vue";
import api from "src/api";

export default {
  props: {
    network: { type: Object, required: true }
  },
  components: {
    CreateNetwork,
    ContainerListInput
  },
  methods: {
    connectContainer(containerId) {
      const input = { networkId: this.network.id, containerId };
      this.$apollo.mutate({
        mutation: api.docker.network.CONNECT_TO_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.network.LIST_NETWORKS }]
      });
    },
    disconnectContainer(containerId) {
      const input = { networkId: this.network.id, containerId };
      this.$apollo.mutate({
        mutation: api.docker.network.DISCONNECT_FROM_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.network.LIST_NETWORKS }]
      });
    }
  }
};
</script>
