
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Strip prefix regex</div>
      <list-input label="Regex" v-model="form.regex" />
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
  regex: [],
},
}
</script>
