<template>
  <div class="q-gutter-md">
    <component
      :is="formChildren.servers"
      ref="servers"
      v-model="form.servers"
      object-key="address"
      label="Servers"
      :rules="[required('You must choose at least one server')]"
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
  },
  methods: {
    validate() {
      return this.$refs.servers.validate();
    }
  }
};
</script>
