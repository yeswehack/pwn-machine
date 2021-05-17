<template>
  <div class="q-gutter-xs">
    <q-badge
      :title="hostBindings.length ? 'Forwarded' : ''"
      :color="hostBindings.length ? 'negative' : 'primary'"
      :key="idx"
      v-for="({ hostBindings, containerPort, protocol }, idx) of ports"
    >
      {{ containerPort }}/{{ protocol.toLowerCase() }}
      <q-tooltip v-for="({ ip, port }, i) of hostBindings" :key="i">
        {{ `${ip}:${port}` }}
      </q-tooltip>
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
