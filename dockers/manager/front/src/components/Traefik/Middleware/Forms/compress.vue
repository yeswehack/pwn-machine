
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Compress</div>
      <list-input label="Excluded content types" v-model="form.excludedContentTypes" />
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
  excludedContentTypes: [],
},
}
</script>
