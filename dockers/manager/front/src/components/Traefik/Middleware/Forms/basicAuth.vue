
<template>
  <div class="column q-gutter-md">
  <div class="text-h6" v-if="!hideTitle">Basic auth</div>
      <q-input label="Header field" v-model="form.headerField" />
      <q-input label="Realm" v-model="form.realm" />
      <q-toggle label="Remove header" v-model="form.removeHeader" />
      <list-input label="Users" v-model="form.users" />
      <q-input label="Users file" v-model="form.usersFile" />
  </div>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
 import ListInput from 'src/components/ListInput.vue';
export default {
    props: {
        hideTitle: {type: Boolean, default: false}
    },
    components: {  ListInput },
    mixins: [DeepForm],
    formDefinition: {
  headerField: null,
  realm: null,
  removeHeader: null,
  users: [],
  usersFile: null,
},
}
</script>
