<template>
  <div class="column q-col-gutter-sm">
    <component
      :is="formChildren.entryPoints"
      v-model="form.entryPoints"
      protocol="udp"
    />
    <component
      :is="formChildren.service"
      ref="service"
      v-model="form.service"
      protocol="udp"
    />
  </div>
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
    validate() {
      return this.$refs.service.validate();
    }
  }
};
</script>
