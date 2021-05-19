
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Replace path</div>
      <q-input label="Path" v-model="form.path" />
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
  path: null,
},
}
</script>
