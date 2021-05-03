<template>
  <div class="q-gutter-md">
    <component
      :is="formChildren.servers"
      v-model="form.servers"
      object-key="address"
      label="Servers"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    servers: ListInput
  }
};
</script>

<style></style>
