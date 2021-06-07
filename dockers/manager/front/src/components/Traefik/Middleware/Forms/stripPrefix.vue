
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Strip prefix</div>
      <q-toggle v-model="form.forceSlash" label="Force slash" />
      <list-input v-model="form.prefixes" label="Prefixes" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';

export default {
    components: {  ListInput },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  forceSlash: null,
  prefixes: [],
},
}
</script>
