<template>
  <div class="column q-gutter-sm">
    <q-toggle v-model="enable" label="Enable networking" />
    <q-toggle v-model="host" label="Host network" />
    <NetworksSelectTable
      v-model="formData.networks"
      :disable="!enable || host"
      class="bg-grey-9"
    />
    <div>
      <ExposedPorts
        v-model="formData.ports"
        :disable="!enable || host"
        class="bg-grey-9"
      />
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import NetworksSelectTable from "./NetworksSelectTable.vue";
import ExposedPorts from "./ExposedPorts.vue";
import DeepForm from "src/mixins/DeepForm.js";

function replaceArray(arr, ...vals) {
  arr.splice(0, arr.length);
  for (const val of vals) {
    arr.push(val);
  }
}

export default {
  components: { NetworksSelectTable, ExposedPorts },
  mixins: [DeepForm],
  data: () => ({
    enable: !this.value.networks.includes("none"),
    host: this.value.networks.includes("host")
  }),
  computed: {
    enableNetwork() {
      return this.formData.enable;
    }
  },
  watch: {
    enableNetwork(v) {
      if (!v) this.formData.host = false;
    },
    enable(v) {
      if (!v) {
        replaceArray(this.formData.networks, "none");
        this.host = false;
      } else if (this.host) {
        replaceArray(this.formData.networks, "host");
      } else {
        replaceArray(this.formData.networks);
      }
    },
    host(v) {
      if (v) {
        this.enable = true;
        replaceArray(this.formData.networks, "host");
      } else if (this.enable) {
        replaceArray(this.formData.networks);
      } else {
        replaceArray(this.formData.networks, "none");
      }
    }
  }
};
</script>
