<template>
  <div class="q-gutter-md">
    <q-select
      label="Service"
      v-model="form.service"
      :options="serviceOptions"
    />
    <q-input type="number" label="Max body size" v-model.number="form.maxBodySize" />
    <mirrors-input v-model="form.mirrors" :services="serviceOptions" />
  </div>
</template>

<script>
import db from "src/gql";
import DeepForm from "src/mixins/DeepForm.js";
import MirrorsInput from "./MirrorsInput.vue"
export default {
  components: { MirrorsInput },
  mixins: [DeepForm],
  apollo: {
    services: {
      query: db.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
  },
  computed: {
    serviceOptions() {
      return this.services.map(s => s.name);
    }
  },
  methods: {
    createDefaultForm(mirroring) {
      const form = {
        maxBodySize: mirroring?.maxBodySize,
        service: mirroring?.service,
        mirrors: mirroring?.mirrors
      };
      return form;
    },
  }
};
</script>

<style></style>
