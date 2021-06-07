<template>
  <div class="q-gutter-md">
    <q-select
      ref="service"
      v-model="form.service"
      label="Service"
      :options="serviceOptions"
      :rules="[required('You must select a service.')]"
    />
    <q-input
      v-model.number="form.maxBodySize"
      type="number"
      label="Max body size"
    />
    <component
      :is="formChildren.mirrors"
      ref="mirrors"
      v-model="form.mirrors"
      :services="serviceOptions"
    />
  </div>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm.js";
import MirrorsInput from "./MirrorsInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    maxBodySize: null,
    service: null,
    mirrors: MirrorsInput
  },
  apollo: {
    services: {
      query: api.traefik.services.LIST_SERVICES,
      update: data => data.traefikServices
    }
  },
  computed: {
    serviceOptions() {
      return (this.services ?? []).map(s => s.name);
    }
  },
  methods: {
    validate() {
      const validators = [
        this.$refs.service.validate(),
        this.$refs.mirrors.validate()
      ];
      return validators.every(x => x);
    }
  }
};
</script>
