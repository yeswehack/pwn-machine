<template>
  <div class="q-gutter-md">
    <list-input v-model="form.servers" object-key="address" label="Servers" />
    <q-select
      :options="[1, 2]"
      v-model="form.proxyProtocol.version"
      label="Proxy procotol version"
    />
    <q-input
      type="number"
      v-model.number="form.terminationDelay"
      label="Termination delay (ms)"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
export default {
  components: { ListInput },
  mixins: [DeepForm],
  methods: {
    createDefaultForm(loadbalancer) {
      const form = {
        servers: loadbalancer?.servers ?? [],
        proxyProtocol: loadbalancer?.proxyProtocol?.version ?? 2,
        terminationDelay: loadbalancer?.terminationDelay ?? 100
      };
      return form;
    }
  }
};
</script>

<style></style>
