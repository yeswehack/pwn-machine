<template>
  <pm-link :label="name" :hash="name" path="/traefik/services" />
</template>

<script>
import PmLink from "src/components/PMLink.vue";

export default {
  components: { PmLink },
  props: {
    name: { type: String, required: true }
  }
};
</script>
