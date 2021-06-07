
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Retry</div>
      <q-input v-model.number="form.attempts" type="number" label="Attempts" />
      <q-input v-model.number="form.initialInterval" type="number" label="Initial interval" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";

export default {
    components: {  },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  attempts: null,
  initialInterval: null,
},
}
</script>
