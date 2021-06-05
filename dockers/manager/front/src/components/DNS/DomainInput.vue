<template>
  <q-select
    label="Domain"
    v-bind="$attrs"
    ref="domainSelect"
    input-debounce="0"
    use-input
    clearable
    :rules="[required('Domain is required')]"
    :options="domainOptions"
    v-model="form"
    @filter="onFilter"
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    dnsRules: {
      query: api.dns.rules.LIST_RULES
    }
  },
  data: () => ({ needle: null }),
  methods: {
    onFilter(v, done) {
      done(() => {
        this.needle = (v ?? "").toLowerCase();
      });
    },
    clear() {
      this.form = null;
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
