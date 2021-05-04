<template>
  <div class="column q-py-sm">
    <div class="row q-col-gutter-md items-stretch justify-start" v-if="network">
      <div class="col col-6 q-gutter-md">
        <KeyValueTable title="IPAM Config" readonly :value="IPAMConfig" />
        <KeyValueTable title="Labels" readonly :value="network.labels" />
      </div>
      <div class="col col-6">
        <ConnectedList :network="network" @needRefresh="refresh" />
      </div>
      <div class="col col-6"></div>
    </div>
    <q-inner-loading :showing="!network">
      <div class="row q-col-gutter-md items-stretch justify-evenly">
        <q-spinner-gears size="50px" color="primary" />
      </div>
    </q-inner-loading>
  </div>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";
import ConnectedList from "src/components/Docker/Network/ConnectedList.vue";
import gql from "src/gql";

export default {
  components: { KeyValueTable, ConnectedList },
  props: {
    name: String
  },
  apollo: {
    network: {
      query: gql.docker.GET_NETWORK,
      variables() {
        return { name: this.name };
      },
      update: data => data.docker.network
    }
  },
  methods: {
    refresh() {
      this.$apollo.queries.network.refetch();
    }
  },
  computed: {
    loading() {
      return this.$apollo.queries.network.loading;
    },
    IPAMConfig() {
      return [
        { key: "Gateway", value: this.network.gateway },
        { key: "Subnet", value: this.network.subnet }
      ];
    }
  }
};
</script>
