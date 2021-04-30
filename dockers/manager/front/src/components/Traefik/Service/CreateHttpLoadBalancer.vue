<template>
  <div class="q-gutter-md">
    <list-input v-model="form.servers" object-key="url" label="Servers" />
    <q-toggle dense v-model="form.passHostHeader" label="Pass Host header" />
    <q-input
      dense
      v-model="form.responseForwarding.flushInterval"
      label="Flush interval"
    />
    <q-input dense v-model="form.serversTransport" label="Server transport" />
    <sticky-input v-model="form.sticky" class="q-pt-md" />
    <health-check-input v-model="form.healthCheck" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
import StickyInput from "./StickyInput.vue";
import HealthCheckInput from "./HealthCheckInput.vue";
export default {
  components: { ListInput, StickyInput, HealthCheckInput },
  mixins: [DeepForm],
  methods: {
    createDefaultForm(loadbalancer) {
      const form = {
        servers: loadbalancer?.servers ?? [],
        sticky: loadbalancer?.sticky ?? {},
        healthCheck: loadbalancer?.healthCheck ?? {},
        responseForwarding: loadbalancer?.responseForwarding ?? {},
        passHostHeader: loadbalancer?.passHostHeader ?? true,
        serversTransport: loadbalancer?.serversTransport
      };
      return form;
    }
  }
};
</script>

<style></style>