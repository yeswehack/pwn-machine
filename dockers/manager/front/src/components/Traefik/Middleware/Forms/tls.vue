
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Tls">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-input v-model="form.ca" label="Ca" />
      <q-toggle v-model="form.caOptional" label="Ca optional" />
      <q-input v-model="form.cert" label="Cert" />
      <q-toggle v-model="form.insecureSkipVerify" label="Insecure skip verify" />
      <q-input v-model="form.key" label="Key" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";

export default {
    components: {  },
    mixins: [DeepForm],
    formDefinition: {
  ca: null,
  caOptional: null,
  cert: null,
  insecureSkipVerify: null,
  key: null,
},
}
</script>
