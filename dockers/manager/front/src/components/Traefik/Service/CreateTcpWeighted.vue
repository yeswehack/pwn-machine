<template>
  <div class="q-gutter-md">
    <component
      ref="service"
      protocol="tcp"
      :is="formChildren.services"
      v-model="form.services"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    services: WeightedInput
  },
  methods: {
    validate() {
      this.$refs.service.validate();
    }
  }
};
</script>
