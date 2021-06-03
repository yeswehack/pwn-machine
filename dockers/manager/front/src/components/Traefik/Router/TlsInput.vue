<template>
  <q-expansion-item expand-separator icon="lock" label="TLS">
    <q-separator />
    <q-card>
      <q-card-section>
        <q-select
          label="Cert resolver"
          :options="resolverOptions"
          emit-value
          map-options
          v-model="form.certResolver"
        />
        <base-grid-input
          :titles="['Domain']"
          gridFormat="1fr"
          :entries="form.domains"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <domain-input
              ref="dnsdomain"
              :disable="certResolver == null"
              v-model="domain"
              @input="addEntry"
              v-if="dnsResolver"
            />
            <q-input
              label="Domain"
              @keypress.enter="addEntry"
              :disable="certResolver == null"
              v-model="domain"
              v-else
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.sans ? entry.sans : entry.main }}
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
  }
};
</script>

<style></style>
