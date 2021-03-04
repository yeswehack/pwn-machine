<template>
  <PMLink path="/docker/networks" :name="name" :color="color" />
</template>

<script>
import PMLink from "src/components/PMLink.vue";
export default {
  components: { PMLink },
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
