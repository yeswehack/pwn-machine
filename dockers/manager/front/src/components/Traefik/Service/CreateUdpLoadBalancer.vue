<template>
  <component
    :is="formChildren.servers"
    v-model="form.servers"
    :titles="['Servers address']"
    :error="error"
  >
    <template #address="props">
      <q-input
        v-model="props.model.address"
        label="Servers address"
        flat
        v-bind="props"
      />
    </template>
  </component>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    servers: ListInput
  },
  data: () => ({ error: null }),
  methods: {
    validate() {
      this.error = "";
      if (this.form.servers.length === 0) {
        this.error = "You must choose at least one server";
        return false;
      }
      return true;
    }
  }
};
</script>
