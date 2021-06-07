<template>
  <q-expansion-item label="Health Check" icon="eva-activity-outline">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="column q-col-gutter-sm">
          <div class="row items-center q-gutter-sm">
            <q-select
              v-model="form.scheme"
              label="protocol"
              class="col col-3"
              :options="['http', 'https']"
            />
            <q-input v-model="form.hostname" label="Hostname" class="col " />
            <q-input
              v-model.number="form.port"
              label="Port"
              class="col col-2"
              type="number"
            />
          </div>
          <q-input v-model="form.path" label="Path" />
          <q-toggle
            v-model="form.followRedirects"
            label="Follow redirects"
            class="col"
          />
          <component :is="formChildren.headers" v-model="form.headers" />
          <div class="row q-gutter-md">
            <q-input v-model="form.interval" label="Interval" class="col" />
            <q-input v-model="form.timeout" label="Timeout" class="col" />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import HeadersInput from "../HeadersInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    hostname: null,
    path: null,
    port: null,
    scheme: null,
    headers: HeadersInput,
    interval: null,
    followRedirects: true,
    timeout: null
  },
  computed: {
    port() {
      return this.form.port;
    }
  },
  watch: {
    port(value) {
      if (value === "") {
        this.form.port = null;
      }
    }
  }
};
</script>
