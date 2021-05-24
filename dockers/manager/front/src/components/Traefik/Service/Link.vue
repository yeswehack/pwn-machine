<template>
  <PMLink path="/traefik/services" :name="name" />
</template>

<script>
import PMLink from "src/components/PMLink.vue";
export default {
  components: { PMLink },
  props: {
    name: { type: String, required: true }
  }
};
</script>
