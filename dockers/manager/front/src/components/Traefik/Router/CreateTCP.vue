<template>
  <q-card-section class="column q-col-gutter-sm">
    <q-input
      v-model="form.rule"
      debounce="100"
      :rules="[validateRule]"
      hint="ex: HostSNI(`example.com`)"
      label="Rule"
    />
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="tcp"
    />
    <component
      :is="formChildren.service"
      v-model="form.service"
      protocol="tcp"
    />
  </q-card-section>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import EntrypointInput from "./EntrypointInput.vue";
import ServiceInput from "./ServiceInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    rule: null,
    entryPoints: EntrypointInput,
    service: ServiceInput,
    tls: null
  },
  methods: {
    validateRule(rule) {
      if (!this.$api.traefik.isValidRule(rule)) {
        return `Syntax error`;
      }
    }
  }
};
</script>

<style></style>
