<template>
  <div class="q-gutter-md">
    <component
      ref="servers"
      :is="formChildren.servers"
      :rules="[validateServers]"
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
  },
  methods: {
    validateServers(v) {
      if (!Array.isArray(v) || v.length == 0) {
        return "You must choose at least one server";
      }
    },
    validate() {
      return this.$refs.servers.validate();
    }
  }
};
</script>

<style></style>
