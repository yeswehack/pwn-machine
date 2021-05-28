<template>
  <pm-link path="/traefik/entrypoints" :hash="name" :label="name" />
</template>

<script>
import PmLink from "src/components/PMLink.vue";
export default {
  components: { PmLink },
  props: { name: String }
};
</script>
