<template>
  <div class="q-gutter-md">
    <component
      :is="formChildren.servers"
      ref="servers"
      v-model="form.servers"
      object-key="address"
      label="Servers address"
      :rules="[required('You must choose at least one server')]"
    />
    <q-select
      v-model="form.proxyProtocol.version"
      label="Proxy procotol version"
      :options="[1, 2]"
    />
    <q-input
      v-model.number="form.terminationDelay"
      label="Termination delay (ms)"
      type="number"
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
