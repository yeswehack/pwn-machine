
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Circuit breaker</div>
      <q-input v-model="form.expression" label="Expression" />
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
  expression: null,
},
}
</script>
