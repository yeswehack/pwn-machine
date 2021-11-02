
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Strip prefix</div>
      <q-toggle v-model="form.forceSlash" label="Force slash" />
      <component :is="formChildren.prefixes" v-model="form.prefixes" label="Prefixes" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import StringListInput from 'src/components/StringListInput.vue';
export default {
    components: {  },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  forceSlash: null,
  prefixes: StringListInput,
},
}
</script>
