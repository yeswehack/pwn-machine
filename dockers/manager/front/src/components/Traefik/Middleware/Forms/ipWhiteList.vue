
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Ip white list</div>
      <component :is="formChildren.ipStrategy" label="Ip strategy" v-model="form.ipStrategy" />
      <list-input label="Source range" v-model="form.sourceRange" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ipStrategy from './ipStrategy.vue';
 import ListInput from 'src/components/ListInput.vue';
export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput, ipStrategy },
    mixins: [DeepForm],
    formDefinition: {
  ipStrategy: ipStrategy,
  sourceRange: [],
},
}
</script>
