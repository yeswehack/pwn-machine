<template>
  <q-expansion-item label="TLS" icon="lock" expand-separator>
    <q-separator />
    <q-card>
      <q-card-section>
        <q-select
          v-model="form.certResolver"
          label="Cert resolver"
          :options="resolverOptions"
          emit-value
          map-options
        />
        <base-grid-input
          :titles="['Domain']"
          grid-format="1fr"
          :entries="form.domains"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <domain-input
              v-if="dnsResolver"
              ref="dnsdomain"
              v-model="domain"
              :disable="certResolver === null"
              @keyup.enter="addEntry"
            />
            <q-input
              v-else
              v-model="domain"
              label="Domain"
              :disable="certResolver === null"
              @keyup.enter="addEntry"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.sans || entry.main }}
            </div>
          </template>
        </base-grid-input>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import { mapGetters } from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";
import DomainInput from "src/components/DNS/DomainInput.vue";

export default {
  components: { BaseGridInput, DomainInput },
  mixins: [DeepForm],
  formDefinition: {
    certResolver: null,
    domains: []
  },
  data() {
    const resolverOptions = [
      { value: null, label: "Disabled" },
      {
        value: "letsencrypt-staging-http",
        label: "Let's Encrypt staging - HTTP"
      },
      {
        value: "letsencrypt-staging-dns",
        label: "Let's Encrypt staging - DNS"
      },
      { value: "letsencrypt-http", label: "Let's Encrypt - HTTP" },
      { value: "letsencrypt-dns", label: "Let's Encrypt - DNS" }
    ];
    return { resolverOptions, domain: null };
  },
  computed: {
    ...mapGetters("certResolver"),
    dnsResolver() {
      return ["letsencrypt-staging-dns", "letsencrypt-dns"].includes(
        this.form.certResolver
      );
    }
  },
  watch: {
    resolver(v) {
      if (v === null) {
        this.form.domains.splice(0, this.form.domains.length);
      }
    }
  },
  methods: {
    addEntry() {
      if (!this.domain) return;
      if (this.domain.startsWith("*.")) {
        this.form.domains.unshift({
          main: this.domain.slice(2),
          sans: this.domain
        });
      } else {
        this.form.domains.unshift({ main: this.domain });
      }
      this.domain = null;
      this.$refs.dnsdomain?.clear();
    },
    removeEntry(idx) {
      this.form.domains.splice(idx, 1);
    }
  }
};
</script>
