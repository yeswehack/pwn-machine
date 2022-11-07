
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Errors</div>
      <q-input v-model="form.query" label="Query" />
      <q-input v-model="form.service" label="Service" />
      <component :is="formChildren.status" v-model="form.status" label="Status" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import StringListInput from 'src/components/StringListInput.vue';
export default {
    components: {  },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  query: null,
  service: null,
  status: StringListInput,
},
}
</script>
