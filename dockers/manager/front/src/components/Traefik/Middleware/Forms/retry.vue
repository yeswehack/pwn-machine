
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Retry</div>
      <q-input type="number" label="Attempts" v-model.number="form.attempts" />
      <q-input type="number" label="Initial interval" v-model.number="form.initialInterval" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";

export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  },
    mixins: [DeepForm],
    formDefinition: {
  attempts: null,
  initialInterval: null,
},
}
</script>
