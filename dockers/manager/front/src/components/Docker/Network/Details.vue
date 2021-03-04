<template>
  <div class="column q-py-sm">
    <div class="row q-col-gutter-md items-stretch justify-evenly">
      <div class="col col-grow" v-if="network.Driver == 'bridge'">
        <KeyValueTable title="IPAM Config" readonly :value="IPAMConfig" />
      </div>
      <div class="col col-grow">
        <ConnectedList :containers="network.Containers" />
      </div>
      <div class="col col-grow">
        <KeyValueTable title="Labels" readonly :value="network.Labels" />
      </div>
    </div>
  </div>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";
import ConnectedList from "src/components/Docker/Network/ConnectedList.vue";
export default {
  components: { KeyValueTable, ConnectedList },
  props: {
    network: Object
  },
  data() {
    const IPAMConfig =
      this.network.IPAM.Config.length > 0 ? this.network.IPAM.Config[0] : {};
    return {
      IPAMConfig
    };
  }
};
</script>
