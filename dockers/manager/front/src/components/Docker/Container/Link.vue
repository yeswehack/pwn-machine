<template>
  <pm-link path="/docker/containers" :hash="name" :label="name"><slot/></pm-link>
</template>

<script>
import PmLink from "src/components/PMLink.vue";

export default {
  components: { PmLink },
  props: { name: String }
};
</script>
