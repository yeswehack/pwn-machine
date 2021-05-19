
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Tls">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-input label="Ca" v-model="form.ca" />
      <q-toggle label="Ca optional" v-model="form.caOptional" />
      <q-input label="Cert" v-model="form.cert" />
      <q-toggle label="Insecure skip verify" v-model="form.insecureSkipVerify" />
      <q-input label="Key" v-model="form.key" />
</div>
        </q-card-section>
        <q-card-section v-if="0">
          <pre>{{form}}</pre>
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
