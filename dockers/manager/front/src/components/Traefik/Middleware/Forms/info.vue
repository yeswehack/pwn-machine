
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Info">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <component :is="formChildren.issuer" v-model="form.issuer" label="Issuer" />
      <q-toggle v-model="form.notAfter" label="Not after" />
      <q-toggle v-model="form.notBefore" label="Not before" />
      <q-toggle v-model="form.sans" label="Sans" />
      <q-toggle v-model="form.serialNumber" label="Serial number" />
      <component :is="formChildren.subject" v-model="form.subject" label="Subject" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import subject from './subject.vue';
 import issuer from './issuer.vue';

export default {
    components: {  subject, issuer },
    mixins: [DeepForm],
    formDefinition: {
  issuer: issuer,
  notAfter: null,
  notBefore: null,
  sans: null,
  serialNumber: null,
  subject: subject,
},
}
</script>
