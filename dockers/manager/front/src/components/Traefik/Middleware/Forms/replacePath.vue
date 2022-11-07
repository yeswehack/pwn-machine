
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Replace path</div>
      <q-input v-model="form.path" label="Path" />
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
  path: null,
},
}
</script>
