<template>
  <div class="column q-col-gutter-sm">
    <q-input
      ref="rule"
      v-model="form.rule"
      label="Rule"
      hint="ex: HostSNI(`example.com`)"
      :rules="[validateRule]"
      debounce="100"
    />
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="tcp"
    />
    <component
      :is="formChildren.service"
      ref="service"
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
    validateRule: v => isValidRule(v) || "Syntax error",
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
