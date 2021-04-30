<template>
  <div class="q-gutter-md">
    <weighted-input v-model="form.services" />
    <sticky-input v-model="form.sticky" class="q-pt-md" />
  </div>
</template>

<script>
import db from "src/gql";
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from './WeightedInput.vue';
import StickyInput from './StickyInput.vue';
export default {
  components: {  WeightedInput, StickyInput },
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
    createDefaultForm(weighted) {
      const form = {
        services: weighted?.services,
        sticky: weighted?.sticky
      };
      return form;
    },
  }
};
</script>

<style></style>
