<template>
  <div class="column q-col-gutter-sm">
    <div class="col row q-gutter-sm">
      <div class="col">
        <q-input
          v-model="form.rule"
          ref="rule"
          debounce="100"
          :rules="[validateRule]"
          hint="ex: Host(`example.com`)"
          label="Rule"
        />
      </div>
      <div class="col col-auto">
        <q-input
          type="number"
          label="Prority"
          placeholder="auto"
          v-model.number="form.priority"
        />
      </div>
    </div>
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="tcp"
    />
    <component
      :is="formChildren.middlewares"
      v-model="form.middlewares"
      protocol="http"
    />
    <component
      ref="service"
      :is="formChildren.service"
      v-model="form.service"
      protocol="http"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import EntrypointInput from "./EntrypointInput.vue";
import ServiceInput from "./ServiceInput.vue";
import MiddlewareInput from "./MiddlewareInput.vue";
import { isValidRule } from "src/traefik";
export default {
  mixins: [DeepForm],
  formDefinition: {
    rule: null,
    entryPoints: EntrypointInput,
    middlewares: MiddlewareInput,
    priority: null,
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
