<template>
  <PMLink path="/traefik/middlewares" :name="name" />
</template>

<script>
import PMLink from "src/components/PMLink.vue";
export default {
  components: { PMLink },
  props: { name: String }
};
</script>
