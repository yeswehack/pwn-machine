
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Ip strategy">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <q-input v-model.number="form.depth" type="number" label="Depth" />
      <component :is="formChildren.excludedIPs" v-model="form.excludedIPs" label="Excludedi ps" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import StringListInput from 'src/components/StringListInput.vue';
export default {
    components: {  },
    mixins: [DeepForm],
    formDefinition: {
  depth: null,
  excludedIPs: StringListInput,
},
}
</script>
