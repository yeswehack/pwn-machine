<template>
  <q-expansion-item label="Health Check" icon="eva-activity-outline">
    <div class="column q-pb-md q-col-gutter-sm">
      <q-input v-model="model" label="URL" :error="!isValidUrl">
        <template v-slot:error>
          Invalid url.
        </template>
      </q-input>
      <q-toggle dense v-model="form.followRedirects" label="Follow redirects" />
      <headers-input v-model="form.headers" />
      <div class="row q-gutter-md">
        <q-input class="col" v-model="form.interval" label="Interval" />
        <q-input class="col" v-model="form.timeout" label="Timeout" />
      </div>
    </div>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import HeadersInput from "../HeadersInput.vue";

export default {
  mixins: [DeepForm],
  components: { HeadersInput },
  computed: {
    isValidUrl() {
      if (!this.model) {
        return true;
      }
      try {
        new URL(this.model);
        return true;
      } catch {
        return false;
      }
    }
  },
  data() {
    return { model: ""};
  },
  watch: {
    model(value) {
      if (value && this.isValidUrl) {
        Object.assign(this.form, this.urlToObject(value))
      }
    }
  },
  methods: {
    urlToObject(u) {
      const url = new URL(u);
      return {
        hostname: url.hostname,
        path: url.pathname,
        scheme: url.protocol.slice(0, -1),
        port: url.port || undefined
      };
    },
    objectToUrl(o){
      const scheme = o.scheme ? `${o.scheme}://` : ''
      const port = o.port ? `:${o.port}` : ''
      const hostname = o.hostname ??  ''
      const path = o.path ??  ''
      
      return `${scheme}${hostname}${port}${path}`
    },
    createDefaultForm(healthCheck) {
      this.model = this.objectToUrl(healthCheck)
      const form = {
        hostname: healthCheck?.hostname,
        path: healthCheck?.path,
        port: healthCheck?.port,
        scheme: healthCheck?.scheme,
        headers: healthCheck?.headers,
        interval: healthCheck?.interval,
        followRedirects: healthCheck?.followRedirects ?? true,
        timeout: healthCheck?.timeout
      };
      return form;
    }
  }
};
</script>

<style></style>
