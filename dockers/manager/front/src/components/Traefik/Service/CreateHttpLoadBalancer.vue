<template>
  <div class="column q-gutter-md">
    <div class="col">
      <component
        ref="servers"
        object-key="url"
        label="Servers url"
        :is="formChildren.servers"
        :rules="[required('You must choose at least one server')]"
        v-model="form.servers"
      />
    </div>

    <div class="col">
      <div class="row q-gutter-xl items-end">
        <div class="col">
          <q-input
            label="Flush interval"
            v-model="form.responseForwarding.flushInterval"
          />
        </div>
        <div class="col-auto">
          <q-toggle
            label="Pass Host header"
            left-label
            v-model="form.passHostHeader"
          />
        </div>
      </div>
    </div>
    <!-- q-input v-model="form.serversTransport" label="Server transport" /-->
    <q-list bordered separator class="rounded-borders">
      <component :is="formChildren.sticky" v-model="form.sticky" />
      <component :is="formChildren.healthCheck" v-model="form.healthCheck" />
    </q-list>
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
    responseForwarding: {
      flushInterval: "100ms"
    },
    passHostHeader: true,
    serversTransport: null
  },
  methods: {
    validate() {
      return this.$refs.servers.validate();
    }
  }
};
</script>
