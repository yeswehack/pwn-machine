<template>
  <div class="column q-col-gutter-sm">
    <q-input
      ref="rule"
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
      ref="service"
      :is="formChildren.service"
      v-model="form.service"
      protocol="tcp"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import EntrypointInput from "./EntrypointInput.vue";
import ServiceInput from "./ServiceInput.vue";
import { isValidRule } from "src/traefik";
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
      if (!isValidRule(rule)) {
        return `Syntax error`;
      }
    },
    validate() {
      const validators = [
        this.$refs.rule.validate(),
        this.$refs.service.validate()
      ];
      return validators.every(x => x);
    }
  }
};
</script>

<style></style>
