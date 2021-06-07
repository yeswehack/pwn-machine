<template>
  <div class="q-gutter-md">
    <component
      ref="servers"
      object-key="address"
      label="Servers"
      :is="formChildren.servers"
      :rules="[required('You must choose at least one server')]"
      v-model="form.servers"
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
