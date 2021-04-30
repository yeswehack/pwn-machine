<template>
  <div class="q-gutter-md">
    <weighted-input v-model="form.services" protocol="udp" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";
export default {
  components: { WeightedInput },
  mixins: [DeepForm],
  methods: {
    createDefaultForm(weighted) {
      const form = {
        services: weighted?.services
      };
      return form;
    }
  }
};
</script>

<style></style>
