<template>
  <PMLink path="/traefik/services" :name="service.name" />
</template>

<script>
import PMLink from "src/components/PMLink.vue";
export default {
  components: { PMLink },
  props: {
    service: { type: Object, required: true }
  }
};
</script>
