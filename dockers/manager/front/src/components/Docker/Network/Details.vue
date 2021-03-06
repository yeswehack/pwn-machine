<template>
  <div class="column q-py-sm">
    <div class="row q-col-gutter-md items-stretch justify-evenly" v-if="!loading">
      <div class="col col-grow" v-if="network.driver == 'bridge'">
        <KeyValueTable title="IPAM Config" readonly :value="IPAMConfig" />
      </div>
      <div class="col col-grow">
        <ConnectedList :connected="network.connectedContainers"  />
      </div>
      <div class="col col-grow">
        <KeyValueTable title="Labels" readonly :value="network.labels" />
      </div>
    </div>
    <q-inner-loading :showing="loading">
      <div class="row q-col-gutter-md items-stretch justify-evenly">
        <q-spinner-gears size="50px" color="primary" />
      </div>
    </q-inner-loading>
  </div>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";
import ConnectedList from "src/components/Docker/Network/ConnectedList.vue";
import gql from "graphql-tag";

export default {
  components: { KeyValueTable, ConnectedList },
  props: {
    name: String
  },
  apollo: {
    network: {
      query: gql`
        query getNetwork($name: String!) {
          docker {
            network(name: $name) {
              name
              driver
              gateway
              subnet
              connectedContainers {
                name
                ipv4
                ipv6
              }
              labels {
                key
                value
              }
            }
          }
        }
      `,
      variables() {
        return { name: this.name };
      },
      update: data => data.docker.network
    }
  },
  computed: {
    loading(){
      return this.$apollo.queries.network.loading
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
