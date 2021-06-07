
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Redirect scheme</div>
      <q-toggle v-model="form.permanent" label="Permanent" />
      <q-input v-model="form.port" label="Port" />
      <q-input v-model="form.scheme" label="Scheme" />
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
  port: null,
  scheme: null,
},
}
</script>
