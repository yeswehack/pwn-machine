<template>
  <q-badge :color="color">
    {{ status }}
  </q-badge>
</template>

<script>
export default {
  props: {
    status: String
  },
  computed: {
    color() {
      switch (this.status.toLowerCase()) {
        case "running":
          return "positive";
        case "created":
        case "restarting":
          return "primary";
        case "paused":
          return "orange";
        case "removing":
        case "exited":
        case "dead":
          return "negative";
      }
      return "primary";
    }
  }
};
</script>
