
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Forward auth</div>
      <q-input v-model="form.address" label="Address" />
      <list-input v-model="form.authRequestHeaders" label="Auth request headers" />
      <list-input v-model="form.authResponseHeaders" label="Auth response headers" />
      <q-input v-model="form.authResponseHeadersRegex" label="Auth response headers regex" />
      <component :is="formChildren.tls" v-model="form.tls" label="Tls" />
      <q-toggle v-model="form.trustForwardHeader" label="Trust forward header" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import tls from './tls.vue';
 import ListInput from 'src/components/ListInput.vue';

export default {
    components: {  ListInput, tls },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
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
