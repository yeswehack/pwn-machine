<template>
  <pm-link path="/docker/networks" :hash="name" :label="name" :color="color">
    <slot />
  </pm-link>
</template>

<script>
import PmLink from "src/components/PMLink.vue";
export default {
  components: { PmLink },
  props: { name: String },
  computed: {
    color() {
      switch (this.name) {
        case "none":
          return "negative";
        case "host":
          return "positive";
        default:
          return "primary";
      }
    }
  }
};
</script>
