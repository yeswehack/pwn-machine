<template>
  <div class="column q-gutter-md">
    <div class="col">
      <component
        :is="formChildren.servers"
        v-model="form.servers"
        :titles="['Servers url']"
        :error="error"
      >
        <template #url="props">
          <q-input
            v-model="props.model.url"
            label="Servers url"
            flat
            v-bind="props"
          />
        </template>
      </component>
    </div>

    <div class="col">
      <div class="row q-gutter-xl items-end">
        <div class="col">
          <q-input
            v-model="form.responseForwarding.flushInterval"
            label="Flush interval"
          />
        </div>
        <div class="col-auto">
          <q-toggle
            v-model="form.passHostHeader"
            label="Pass Host header"
            left-label
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
  data: () => ({ error: null }),
  methods: {
    validate() {
      this.error = "";
      if (this.form.servers.length === 0) {
        this.error = "You must choose at least one server";
        return false;
      }
      return true;
    }
  }
};
</script>
