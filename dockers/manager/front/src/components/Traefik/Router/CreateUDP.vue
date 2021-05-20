<template>
  <q-card-section class="column q-col-gutter-sm">
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="udp"
    />
    <component
      :is="formChildren.service"
      v-model="form.service"
      protocol="udp"
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
