<template>
  <q-badge outline  class="text-white" :style="{'border-color': color}">{{ protocol }} </q-badge>
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
          return "var(--q-color-primary)";
        case "tcp":
          return "var(--q-color-secondary)";
        case "udp":
          return "var(--q-color-accent)";
        default:
          return "var(--q-color-negative)";
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.status {
  color: white ;
}
</style>
