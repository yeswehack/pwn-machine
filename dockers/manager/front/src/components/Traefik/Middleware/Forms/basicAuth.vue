
<template>
  <div class="column q-gutter-md">
  <div v-if="!hideTitle" class="text-h6">Basic auth</div>
      <q-input v-model="form.headerField" label="Header field" />
      <q-input v-model="form.realm" label="Realm" />
      <q-toggle v-model="form.removeHeader" label="Remove header" />
      <list-input v-model="form.users" label="Users" />
      <q-input v-model="form.usersFile" label="Users file" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';

export default {
    components: {  ListInput },
    mixins: [DeepForm],
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    formDefinition: {
  headerField: null,
  realm: null,
  removeHeader: null,
  users: [],
  usersFile: null,
},
}
</script>
