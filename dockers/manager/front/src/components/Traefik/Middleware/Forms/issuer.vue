
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Issuer">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-toggle label="Common name" v-model="form.commonName" />
      <q-toggle label="Country" v-model="form.country" />
      <q-toggle label="Domain component" v-model="form.domainComponent" />
      <q-toggle label="Locality" v-model="form.locality" />
      <q-toggle label="Organization" v-model="form.organization" />
      <q-toggle label="Province" v-model="form.province" />
      <q-toggle label="Serial number" v-model="form.serialNumber" />
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
  commonName: null,
  country: null,
  domainComponent: null,
  locality: null,
  organization: null,
  province: null,
  serialNumber: null,
},
}
</script>
