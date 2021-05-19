
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Buffering</div>
      <q-input type="number" label="Max request body bytes" v-model.number="form.maxRequestBodyBytes" />
      <q-input type="number" label="Max response body bytes" v-model.number="form.maxResponseBodyBytes" />
      <q-input type="number" label="Mem request body bytes" v-model.number="form.memRequestBodyBytes" />
      <q-input type="number" label="Mem response body bytes" v-model.number="form.memResponseBodyBytes" />
      <q-input label="Retry expression" v-model="form.retryExpression" />
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
  maxRequestBodyBytes: null,
  maxResponseBodyBytes: null,
  memRequestBodyBytes: null,
  memResponseBodyBytes: null,
  retryExpression: null,
},
}
</script>
