<template>
  <pm-link path="/dns/zones" :hash="name" :label="name" />
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
