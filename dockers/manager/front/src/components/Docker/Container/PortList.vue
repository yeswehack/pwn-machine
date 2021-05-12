<template>
  <div class="q-gutter-xs">
    <q-badge
      :title="hostPort ? 'Forwarded' : ''"
      :color="hostPort ? 'negative' : 'primary'"
      :key="idx"
      v-for="({ hostPort, containerPort, protocol }, idx) of ports"
    >
      {{ containerPort }}/{{ protocol.toLowerCase() }}
    </q-badge>
    <q-badge title="host driver" color="positive" label="all" v-if="host" />
  </div>
</template>

<script>
export default {
  props: {
    ports: Array,
    host: { type: Boolean, default: false }
  }
};
</script>

<style></style>
