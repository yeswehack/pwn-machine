<template>
  <q-badge :color="color">{{ type }} </q-badge>
</template>

<script>
export default {
  props: { type: String },
  computed: {
    color() {
      switch (this.type) {
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
