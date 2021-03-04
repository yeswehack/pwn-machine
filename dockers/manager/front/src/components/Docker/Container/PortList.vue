<template>
  <div class="q-gutter-xs">
    <q-badge
      :title="exposed ? 'Forwarded' : ''"
      :color="exposed ? 'negative' : 'primary'"
      :key="port"
      v-for="[port, exposed] of Object.entries(ports)"
    >
      {{ port }}
    </q-badge>
    <q-badge title="host driver" color="positive" label="all" v-if="host" />
  </div>
</template>

<script>
export default {
  props: {
    settings: Object
  },
  computed: {
    ports() {
      return this.settings.Ports;
    },
    host() {
      return "host" in this.settings.Networks;
    }
  }
};
</script>

<style></style>
