
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Errors</div>
      <q-input v-model="form.query" label="Query" />
      <q-input v-model="form.service" label="Service" />
      <list-input v-model="form.status" label="Status" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';

export default {
    components: {  ListInput },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  query: null,
  service: null,
  status: [],
},
}
</script>
