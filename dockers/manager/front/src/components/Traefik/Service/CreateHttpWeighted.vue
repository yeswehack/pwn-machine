<template>
  <div class="q-gutter-md">
    <component :is="formChildren.services" v-model="form.services" protocol="http"/>
    <component :is="formChildren.sticky" v-model="form.sticky" class="q-pt-md" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from './WeightedInput.vue';
import StickyInput from './StickyInput.vue';
export default {
  mixins: [DeepForm],
  formDefinition: {
    services: WeightedInput,
    sticky: StickyInput
  }
};
</script>

<style></style>
