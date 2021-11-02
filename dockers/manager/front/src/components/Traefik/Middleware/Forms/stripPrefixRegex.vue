
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Strip prefix regex</div>
      <component :is="formChildren.regex" v-model="form.regex" label="Regex" />
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
  regex: StringListInput,
},
}
</script>
