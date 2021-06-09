<template>
  <q-select
    ref="portSelect"
    v-model.number="form"
    clearable
    use-input
    :rules="[required('This field is required')]"
    :options="portOptions"
    new-value-mode="add"
    label="Port to expose"
    map-options
    emit-value
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  props: {
    container: { type: Object, default: null }
  },
  computed: {
    portOptions() {
      return (this.container?.ports ?? [])
        .filter(p => p.protocol === "tcp")
        .map(p => ({
          label: p.containerPort,
          value: p.containerPort,
          protocol: p.protocol
        }));
    }
  },
  methods: {
    validate() {
      return this.$refs.portSelect.validate();
    }
  }
};
</script>
