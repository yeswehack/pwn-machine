<template>
  <q-select
    label="Domain"
    v-bind="$attrs"
    ref="domainSelect"
    input-debounce="0"
    use-input
    clearable
    :rules="[required('Domain is required')]"
    new-value-mode="add"
    :options="domainOptions"
    v-model="form"
    @filter="onFilter"
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import { required } from "src/utils/validators.js";
export default {
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    dnsRules: {
      query: api.dns.rules.LIST_RULES
    }
  },
  data() {
    return { needle: null, required };
  },
  methods: {
    onFilter(v, done) {
      done(() => {
        this.needle = (v ?? "").toLowerCase();
      });
    }
  },
  computed: {
    domainOptions() {
      return (this.dnsRules ?? [])
        .filter(r => ["A", "AAAA", "CNAME"].includes(r.type))
        .map(r => r.name.slice(0, -1))
        .filter(name => name.includes(this.needle));
    }
  }
};
</script>

<style></style>
