
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Rate limit</div>
      <q-input v-model.number="form.average" type="number" label="Average" />
      <q-input v-model.number="form.burst" type="number" label="Burst" />
      <q-input v-model.number="form.period" type="number" label="Period" />
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
  average: null,
  burst: null,
  period: null,
  sourceCriterion: sourceCriterion,
},
}
</script>
