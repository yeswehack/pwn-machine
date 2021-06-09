
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Passtls client cert</div>
      <component :is="formChildren.info" v-model="form.info" label="Info" />
      <q-toggle v-model="form.pem" label="Pem" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import info from './info.vue';

export default {
    components: {  info },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  info: info,
  pem: null,
},
}
</script>
