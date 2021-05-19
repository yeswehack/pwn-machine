
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Passtls client cert</div>
      <component :is="formChildren.info" label="Info" v-model="form.info" />
      <q-toggle label="Pem" v-model="form.pem" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import info from './info.vue';
export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  info },
    mixins: [DeepForm],
    formDefinition: {
  info: info,
  pem: null,
},
}
</script>
