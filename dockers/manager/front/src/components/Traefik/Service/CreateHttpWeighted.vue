<template>
  <div class="q-gutter-md">
    <component
      ref="service"
      :is="formChildren.services"
      v-model="form.services"
      protocol="http"
    />
    <q-list separator class="rounded-borders"  bordered>
      <component
        :is="formChildren.sticky"
        v-model="form.sticky"
      />
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import WeightedInput from "./WeightedInput.vue";
import StickyInput from "./StickyInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    services: WeightedInput,
    sticky: StickyInput
  },
  methods: {
    validate() {
      this.$refs.service.validate();
    }
  }
};
</script>

<style></style>
