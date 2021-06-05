<template>
  <q-expansion-item label="Health Check" icon="eva-activity-outline">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="column q-col-gutter-sm">
          <div class="row items-center q-gutter-sm">
            <q-select
              label="protocol"
              class="col col-3"
              :options="['http', 'https']"
              v-model="form.scheme"
            />
            <q-input label="Hostname" class="col " v-model="form.hostname" />
            <q-input
              label="Port"
              class="col col-2"
              type="number"
              v-model.number="form.port"
            />
          </div>
          <q-input label="Path" v-model="form.path" />
          <q-toggle
            label="Follow redirects"
            class="col"
            v-model="form.followRedirects"
          />
          <component :is="formChildren.headers" v-model="form.headers" />
          <div class="row q-gutter-md">
            <q-input label="Interval" class="col" v-model="form.interval" />
            <q-input label="Timeout" class="col" v-model="form.timeout" />
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
