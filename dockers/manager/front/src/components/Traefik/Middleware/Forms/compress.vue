
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Compress</div>
      <component :is="formChildren.excludedContentTypes" v-model="form.excludedContentTypes" label="Excluded content types" />
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
  excludedContentTypes: StringListInput,
},
}
</script>
