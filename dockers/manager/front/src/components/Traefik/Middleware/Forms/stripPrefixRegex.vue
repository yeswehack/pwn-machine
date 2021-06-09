
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Strip prefix regex</div>
      <list-input v-model="form.regex" label="Regex" />
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
  regex: [],
},
}
</script>
