
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Errors</div>
      <q-input label="Query" v-model="form.query" />
      <q-input label="Service" v-model="form.service" />
      <list-input label="Status" v-model="form.status" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';

export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput },
    mixins: [DeepForm],
    formDefinition: {
  query: null,
  service: null,
  status: [],
},
}
</script>
