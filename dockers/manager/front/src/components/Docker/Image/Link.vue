<template>
  <PMLink path="/docker/images" :name="fullName" />
</template>

<script>
import PMLink from "src/components/PMLink.vue";
export default {
  components: { PMLink },
  props: { name: String },
  computed: {
    fullName(){
      return this.name.includes(":") ? this.name : `${this.name}:latest`
    }
  }
};
</script>
