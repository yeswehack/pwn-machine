<template>
  <div class="q-gutter-md">
    <q-select
      label="Service"
      v-model="form.service"
      :options="serviceOptions"
    />
    <q-input type="number" label="Max body size" v-model.number="form.maxBodySize" />
    <component :is="formChildren.mirrors" :services="serviceOptions" v-model="form.mirrors"/>
  </div>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm.js";
import MirrorsInput from "./MirrorsInput.vue"
export default {
  mixins: [DeepForm],
  apollo: {
    services: {
      query: api.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
  },
  formDefinition: {
    maxBodySize: null,
    service: null,
    mirrors: MirrorsInput
  },
  computed: {
    serviceOptions() {
      return (this.services ?? []).map(s => s.name);
    }
  },
};
</script>

<style></style>
