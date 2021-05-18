<template>
  <div class="row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">{{ network.name }}</div>
            <q-space />
            <help-link
              href="https://docs.docker.com/engine/reference/commandline/network_create/"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <ipam-input readonly :value="network.ipam" />
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <label-input readonly :value="network.labels" />
        </q-card-section>
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section>
          <container-list-input
            @add="connectContainer"
            @remove="disconnectContainer"
            :value="network.usingContainers"
            title="Connected containers"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import IpamInput from "./IpamInput.vue";
import LabelInput from "../LabelInput.vue";
import HelpLink from "src/components/HelpLink.vue";
import ContainerListInput from "../ContainerListInput.vue";
import api from "src/api";

export default {
  props: {
    network: { type: Object, required: true }
  },
  components: {
    IpamInput,
    LabelInput,
    HelpLink,
    ContainerListInput
  },
  methods: {
    refresh() {
      this.$apollo.queries.network.refetch();
    },
    connectContainer(containerId) {
      const input = { networkId: this.network.id, containerId };
      this.$apollo.mutate({
        mutation: api.docker.CONNECT_TO_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.GET_NETWORKS }]
      });
    },
    disconnectContainer(containerId) {
      const input = { networkId: this.network.id, containerId };
      this.$apollo.mutate({
        mutation: api.docker.DISCONNECT_FROM_NETWORK,
        variables: { input },
        refetchQueries: [{ query: api.docker.GET_NETWORKS }]
      });
    }
  }
};
</script>
