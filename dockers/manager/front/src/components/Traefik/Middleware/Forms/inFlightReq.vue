
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">In flight req</div>
      <q-input v-model.number="form.amount" type="number" label="Amount" />
      <component :is="formChildren.sourceCriterion" v-model="form.sourceCriterion" label="Source criterion" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import sourceCriterion from './sourceCriterion.vue';

export default {
    components: {  sourceCriterion },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  amount: null,
  sourceCriterion: sourceCriterion,
},
}
</script>
