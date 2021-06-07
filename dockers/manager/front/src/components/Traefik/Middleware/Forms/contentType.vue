
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Content type</div>
      <q-toggle v-model="form.autoDetect" label="Auto detect" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";

export default {
    components: {  },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  autoDetect: null,
},
}
</script>
