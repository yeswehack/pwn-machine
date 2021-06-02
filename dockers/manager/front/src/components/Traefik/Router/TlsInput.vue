<template>
  <q-expansion-item expand-separator icon="lock" label="TLS">
    <q-separator />
    <q-card>
      <q-card-section>
        <q-select
          label="Cert resolver"
          :options="resolverOptions"
          v-model="form.resolver"
        />
        <component :is="formChildren.domain" :disable="form.resolver == 'no-tls'" v-model="form.domain" />
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";
import DomainInput from "src/components/DNS/DomainInput.vue";
export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  formDefinition: {
    resolver: "no-tls",
    domain: DomainInput
  },
  data() {
    const resolverOptions = [
      "no-tls",
      "letsencrypt-staging-http",
      "letsencrypt-staging-dns",
      "letsencrypt-http",
      "letsencrypt-dns"
    ];
    return { resolverOptions };
  }
};
</script>

<style></style>
