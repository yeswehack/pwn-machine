
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Forward auth</div>
      <q-input label="Address" v-model="form.address" />
      <list-input label="Auth request headers" v-model="form.authRequestHeaders" />
      <list-input label="Auth response headers" v-model="form.authResponseHeaders" />
      <q-input label="Auth response headers regex" v-model="form.authResponseHeadersRegex" />
      <component :is="formChildren.tls" label="Tls" v-model="form.tls" />
      <q-toggle label="Trust forward header" v-model="form.trustForwardHeader" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import tls from './tls.vue';
 import ListInput from 'src/components/ListInput.vue';

export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput, tls },
    mixins: [DeepForm],
    formDefinition: {
  address: null,
  authRequestHeaders: [],
  authResponseHeaders: [],
  authResponseHeadersRegex: null,
  tls: tls,
  trustForwardHeader: null,
},
}
</script>
