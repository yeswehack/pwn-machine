
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Info">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <component :is="formChildren.issuer" label="Issuer" v-model="form.issuer" />
      <q-toggle label="Not after" v-model="form.notAfter" />
      <q-toggle label="Not before" v-model="form.notBefore" />
      <q-toggle label="Sans" v-model="form.sans" />
      <q-toggle label="Serial number" v-model="form.serialNumber" />
      <component :is="formChildren.subject" label="Subject" v-model="form.subject" />
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
