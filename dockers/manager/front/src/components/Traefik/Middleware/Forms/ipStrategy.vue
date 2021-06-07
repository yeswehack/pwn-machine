
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Ip strategy">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-input v-model.number="form.depth" type="number" label="Depth" />
      <list-input v-model="form.excludedIPs" label="Excludedi ps" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';

export default {
    components: {  ListInput },
    mixins: [DeepForm],
    formDefinition: {
  depth: null,
  excludedIPs: [],
},
}
</script>
