
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Compress</div>
      <list-input v-model="form.excludedContentTypes" label="Excluded content types" />
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
  excludedContentTypes: [],
},
}
</script>
