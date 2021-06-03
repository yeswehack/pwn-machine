<template>
  <div class="q-gutter-sm">
    <div class="col row">
      <div class="col q-mr-sm">
        <q-input
          v-model="form.rule"
          ref="rule"
          debounce="100"
          :rules="[validateRule]"
          hint="ex: Host(`example.com`)"
          label="Rule"
        />
      </div>
      <div class="col col-3">
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
    <q-list separator class="rounded-borders" bordered>
      <component ref="tls" :is="formChildren.tls" v-model="form.tls" />
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import EntrypointInput from "./EntrypointInput.vue";
import ServiceInput from "./ServiceInput.vue";
import MiddlewareInput from "./MiddlewareInput.vue";
import TlsInput from "./TlsInput.vue";
import { isValidRule } from "src/traefik";
export default {
  mixins: [DeepForm],
  formDefinition: {
    rule: 'Host(`example.com`) && PathPrefix(`/`)',
    entryPoints: EntrypointInput,
    middlewares: MiddlewareInput,
    priority: null,
    service: ServiceInput,
    tls: TlsInput
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
