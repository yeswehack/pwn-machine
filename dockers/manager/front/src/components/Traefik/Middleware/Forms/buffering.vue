
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Buffering</div>
      <q-input v-model.number="form.maxRequestBodyBytes" type="number" label="Max request body bytes" />
      <q-input v-model.number="form.maxResponseBodyBytes" type="number" label="Max response body bytes" />
      <q-input v-model.number="form.memRequestBodyBytes" type="number" label="Mem request body bytes" />
      <q-input v-model.number="form.memResponseBodyBytes" type="number" label="Mem response body bytes" />
      <q-input v-model="form.retryExpression" label="Retry expression" />
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
  maxRequestBodyBytes: null,
  maxResponseBodyBytes: null,
  memRequestBodyBytes: null,
  memResponseBodyBytes: null,
  retryExpression: null,
},
}
</script>
