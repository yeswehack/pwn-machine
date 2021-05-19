
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Rate limit</div>
      <q-input type="number" label="Average" v-model.number="form.average" />
      <q-input type="number" label="Burst" v-model.number="form.burst" />
      <q-input type="number" label="Period" v-model.number="form.period" />
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
  average: null,
  burst: null,
  period: null,
  sourceCriterion: sourceCriterion,
},
}
</script>
