<template>
  <div class="q-gutter-sm">
    <div class="col row">
      <div class="col q-mr-sm">
        <q-input
          ref="rule"
          label="Rule"
          hint="ex: Host(`example.com`)"
          :rules="[validateRule]"
          v-model="form.rule"
          debounce="100"
        />
      </div>
      <div class="col col-3">
        <q-input
          label="Prority"
          placeholder="auto"
          type="number"
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
    <q-list separator bordered class="rounded-borders">
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
    rule: "Host(`example.com`) && PathPrefix(`/`)",
    entryPoints: EntrypointInput,
    middlewares: MiddlewareInput,
    priority: null,
    service: ServiceInput,
    tls: TlsInput
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
