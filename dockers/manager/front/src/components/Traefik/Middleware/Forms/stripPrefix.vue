
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Strip prefix</div>
      <q-toggle label="Force slash" v-model="form.forceSlash" />
      <list-input label="Prefixes" v-model="form.prefixes" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';
export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput },
    mixins: [DeepForm],
    formDefinition: {
  forceSlash: null,
  prefixes: [],
},
}
</script>
