
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Chain</div>
      <list-input v-model="form.middlewares" label="Middlewares" />
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
  middlewares: [],
},
}
</script>
