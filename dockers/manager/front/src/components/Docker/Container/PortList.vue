<template>
  <div class="q-gutter-xs">
    <q-badge
      :title="hostPort ? 'Forwarded' : ''"
      :color="hostPort ? 'negative' : 'primary'"
      :key="idx"
      v-for="[idx, { hostPort, containerPort, protocol }] of ports.entries()"
    >
      {{ containerPort }}/{{protocol}}
    </q-badge>
    <q-badge title="host driver" color="positive" label="all" v-if="host" />
  </div>
</template>

<script>
export default {
  props: {
    ports: Array,
    host: { type: Boolean, default: false }
  },
};
</script>

<style></style>
