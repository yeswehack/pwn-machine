
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Circuit breaker</div>
      <q-input label="Expression" v-model="form.expression" />
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
  expression: null,
},
}
</script>
