
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Add prefix</div>
      <q-input label="Prefix" v-model="form.prefix" />
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
  prefix: null,
},
}
</script>
