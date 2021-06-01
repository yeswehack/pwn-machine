<template>
  <q-select
    ref="select"
    :options="options"
    :rules="[requiredArray('Please choose a container')]"
    v-model="form"
    label="Container"
    clearable
  />
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import { requiredArray } from "src/utils/validators.js";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  data() {
    return { requiredArray };
  },
  apollo: {
    containers: {
      query: api.docker.containers.LIST_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  computed: {
    options() {
      return (this.containers ?? []).map(c => c.name);
    }
  },
  methods: {
    validate() {
      return this.$refs.select.validate();
    }
  }
};
</script>
