
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Redirect regex</div>
      <q-toggle label="Permanent" v-model="form.permanent" />
      <q-input label="Regex" v-model="form.regex" />
      <q-input label="Replacement" v-model="form.replacement" />
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
  permanent: null,
  regex: null,
  replacement: null,
},
}
</script>
