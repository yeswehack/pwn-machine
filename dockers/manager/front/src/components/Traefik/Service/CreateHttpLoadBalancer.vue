<template>
  <div class="q-gutter-md">
    <component :is="formChildren.servers" object-key="url" v-model="form.servers" label="Servers url"/>
    <q-toggle  v-model="form.passHostHeader" label="Pass Host header" />
    <q-input
      
      v-model="form.responseForwarding.flushInterval"
      label="Flush interval"
    />
    <q-input  v-model="form.serversTransport" label="Server transport" />
    <component :is="formChildren.sticky" v-model="form.sticky"/>
    <component :is="formChildren.healthCheck" v-model="form.healthCheck" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
import StickyInput from "./StickyInput.vue";
import HealthCheckInput from "./HealthCheckInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    servers: ListInput,
    sticky: StickyInput,
    healthCheck: HealthCheckInput,
    responseForwarding: {},
    passHostHeader: true,
    serversTransport: null
  }
};
</script>

<style></style>
