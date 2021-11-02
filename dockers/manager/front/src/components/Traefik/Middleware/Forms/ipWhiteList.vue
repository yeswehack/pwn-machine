
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Ip white list</div>
      <component :is="formChildren.ipStrategy" v-model="form.ipStrategy" label="Ip strategy" />
      <component :is="formChildren.sourceRange" v-model="form.sourceRange" label="Source range" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import ipStrategy from './ipStrategy.vue';
import StringListInput from 'src/components/StringListInput.vue';
export default {
    components: {  ipStrategy },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  ipStrategy: ipStrategy,
  sourceRange: StringListInput,
},
}
</script>
