
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Add prefix</div>
      <q-input v-model="form.prefix" label="Prefix" />
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
  prefix: null,
},
}
</script>
