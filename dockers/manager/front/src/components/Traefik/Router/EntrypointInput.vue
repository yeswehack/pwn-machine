<template>
  <q-select
    v-model="form"
    multiple
    use-chips
    :hint="form.length ? '' : 'all'"
    :options="relevantEntrypoints"
    label="Entrypoint"
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";

export default {
  props: { protocol: { type: String, default: null } },
  mixins: [DeepForm],
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
