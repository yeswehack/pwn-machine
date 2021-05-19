
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Redirect scheme</div>
      <q-toggle label="Permanent" v-model="form.permanent" />
      <q-input label="Port" v-model="form.port" />
      <q-input label="Scheme" v-model="form.scheme" />
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
  port: null,
  scheme: null,
},
}
</script>
