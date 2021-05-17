<template>
  <q-select :options="options" v-model="form" label="Container" clearable />
</template>

<script>
import gql from "src/api";
import DeepForm from "src/mixins/DeepForm";
export default {
  mixins: [DeepForm],
  formDefinition: null,
  data() {
    return {};
  },
  apollo: {
    containers: {
      query: gql.docker.GET_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  computed: {
    options() {
      return (this.containers ?? []).map(c => c.name);
    }
  }
};
</script>
