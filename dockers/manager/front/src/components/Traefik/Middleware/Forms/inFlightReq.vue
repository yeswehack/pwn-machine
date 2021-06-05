
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">In flight req</div>
      <q-input type="number" label="Amount" v-model.number="form.amount" />
      <component :is="formChildren.sourceCriterion" label="Source criterion" v-model="form.sourceCriterion" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import sourceCriterion from './sourceCriterion.vue';

export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  sourceCriterion },
    mixins: [DeepForm],
    formDefinition: {
  amount: null,
  sourceCriterion: sourceCriterion,
},
}
</script>
