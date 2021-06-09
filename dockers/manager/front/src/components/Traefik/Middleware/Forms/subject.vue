
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Subject">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-toggle v-model="form.commonName" label="Common name" />
      <q-toggle v-model="form.country" label="Country" />
      <q-toggle v-model="form.domainComponent" label="Domain component" />
      <q-toggle v-model="form.locality" label="Locality" />
      <q-toggle v-model="form.organization" label="Organization" />
      <q-toggle v-model="form.province" label="Province" />
      <q-toggle v-model="form.serialNumber" label="Serial number" />
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
