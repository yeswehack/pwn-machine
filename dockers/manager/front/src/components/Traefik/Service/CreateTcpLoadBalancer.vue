<template>
  <div class="q-gutter-md">
    <component
      ref="servers"
      :rules="[validateServers]"
      :is="formChildren.servers"
      v-model="form.servers"
      object-key="address"
      label="Servers address"
    />
    <q-select
      :options="[1, 2]"
      v-model="form.proxyProtocol.version"
      label="Proxy procotol version"
    />
    <q-input
      type="number"
      v-model.number="form.terminationDelay"
      label="Termination delay (ms)"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    servers: ListInput,
    proxyProtocol: {
      version: 2
    },
    terminationDelay: 100
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
