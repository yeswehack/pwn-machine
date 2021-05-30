<template>
  <q-select ref="select" :options="options" :rules="[notEmpty]" v-model="form" label="Container" clearable />
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
export default {
  mixins: [DeepForm],
  formDefinition: null,
  data() {
    return {};
  },
  apollo: {
    containers: {
      query: api.docker.containers.LIST_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  computed: {
    options() {
      return (this.containers ?? []).map(c => c.name);
    }
  },
  methods:{
    notEmpty(v){
      if (!v){
        return "Please choose a container"
      }
    },
    validate(){
      return this.$refs.select.validate()
    }
  }
};
</script>
