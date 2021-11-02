
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Chain</div>
      <component :is="formChildren.middlewares" v-model="form.middlewares" label="Middlewares" />
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
  middlewares: StringListInput,
},
}
</script>
