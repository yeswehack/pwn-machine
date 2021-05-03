<template>
  <div class="q-gutter-md">
    <component :is="formChildren.services" v-model="form.services"  protocol="tcp"/>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    services: WeightedInput
  }
};
</script>

<style></style>
