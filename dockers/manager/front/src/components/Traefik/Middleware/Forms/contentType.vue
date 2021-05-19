
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Content type</div>
      <q-toggle label="Auto detect" v-model="form.autoDetect" />
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
  autoDetect: null,
},
}
</script>
