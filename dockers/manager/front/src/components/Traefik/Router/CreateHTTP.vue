<template>
  <q-card-section class="column q-col-gutter-sm">
    <div class="row q-gutter-sm">
      <div class="col">
        <q-input
          v-model="form.rule"
          debounce="100"
          :rules="[validateRule]"
          hint="ex: Host(`example.com`)"
          label="Rule"
        />
      </div>
      <div class="col col-auto">
        <q-input type="number" label="Prority" v-model.number="form.prority" />
      </div>
    </div>
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="tcp"
    />
    <component :is="formChildren.service" v-model="form.service" protocol="http" />
    <component :is="formChildren.middlewares" v-model="form.middlewares" protocol="http" />
  </q-card-section>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import EntrypointInput from "./EntrypointInput.vue";
import ServiceInput from './ServiceInput.vue';
import MiddlewareInput from './MiddlewareInput.vue';
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
      if (!this.$api.traefik.isValidRule(rule)) {
        return `Syntax error`;
      }
    }
  }
};
</script>

<style></style>
