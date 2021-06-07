<template>
  <div class="q-gutter-md">
    <component
      ref="servers"
      object-key="address"
      label="Servers address"
      :is="formChildren.servers"
      :rules="[required('You must choose at least one server')]"
      v-model="form.servers"
    />
    <q-select
      label="Proxy procotol version"
      :options="[1, 2]"
      v-model="form.proxyProtocol.version"
    />
    <q-input
      label="Termination delay (ms)"
      type="number"
      v-model.number="form.terminationDelay"
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
    validate() {
      return this.$refs.servers.validate();
    }
  }
};
</script>
