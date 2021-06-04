<template>
  <q-select
    clearable
    use-input
    ref="portSelect"
    :rules="[required]"
    :options="portOptions"
    new-value-mode="add"
    label="Port to expose"
    v-model.number="form"
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
    container: { type: Object, required: false }
  },
  methods: {
    required(v) {
      if (!v) {
        return "This field is required";
      }
    },
    validate() {
      return this.$refs.portSelect.validate();
    }
  },
  computed: {
    portOptions() {
      return (this.container?.ports ?? [])
        .filter(p => p.protocol == "tcp")
        .map(p => {
          return {
            label: p.containerPort,
            value: p.containerPort,
            protocol: p.protocol
          };
        });
    }
  }
};
</script>

<style></style>
