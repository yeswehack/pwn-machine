<template>
  <div class="q-gutter-md">
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
