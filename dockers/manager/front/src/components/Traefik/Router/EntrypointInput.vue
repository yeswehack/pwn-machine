<template>
  <q-select
    v-model="form"
    label="Entrypoint"
    :hint="form.length ? '' : 'all'"
    use-chips
    :options="relevantEntrypoints"
    multiple
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";

export default {
  mixins: [DeepForm],
  props: {
    protocol: { type: String, default: null }
  },
  formDefinition: [],
  apollo: {
    entrypoints: {
      query: api.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    }
  },
  computed: {
    relevantEntrypoints() {
      return (this.entrypoints ?? [])
        .filter(ep => ep.protocol === this.protocol)
        .map(ep => ep.name);
    }
  }
};
</script>
