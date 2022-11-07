<template>
  <q-badge
    outline
    class="text-white"
    :style="`border-color: var(--q-color-${color})`"
  >
    {{ protocol }}
  </q-badge>
</template>

<script>
export default {
  props: {
    protocol: { type: String, required: true }
  },
  computed: {
    color() {
      const colors = {
        http: "primary",
        tcp: "secondary",
        udp: "accent"
      };
      return colors[this.protocol] ?? "negative";
    }
  }
};
</script>
