<template>
  <q-badge :color="color">{{ protocol }} </q-badge>
</template>

<script>
export default {
  props: {
    protocol: { type: String, required: true }
  },
  computed: {
    color() {
      switch (this.protocol) {
        case "http":
          return "primary";
        case "tcp":
          return "secondary";
        case "udp":
          return "accent";
        default:
          return "negative";
      }
    }
  }
};
</script>

<style></style>
