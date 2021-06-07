
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Redirect regex</div>
      <q-toggle v-model="form.permanent" label="Permanent" />
      <q-input v-model="form.regex" label="Regex" />
      <q-input v-model="form.replacement" label="Replacement" />
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
  permanent: null,
  regex: null,
  replacement: null,
},
}
</script>
