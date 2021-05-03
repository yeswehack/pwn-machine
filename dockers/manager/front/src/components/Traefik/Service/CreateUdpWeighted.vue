<template>
  <div class="q-gutter-md">
    <component :is="formChildren.weighted" v-model="form.services" protocol="udp" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    weighted: WeightedInput
  }
};
</script>

<style></style>
