<template>
  <div class="q-gutter-md">
    <component
      :is="formChildren.weighted"
      ref="services"
      v-model="form.services"
      protocol="udp"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    weighted: WeightedInput
  },
  methods: {
    validate() {
      return this.$refs.services.validate();
    }
  }
};
</script>
