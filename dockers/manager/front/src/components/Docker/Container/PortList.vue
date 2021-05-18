<template>
  <div class="q-gutter-xs">
    <q-badge
      :color="hostBindings.length ? 'negative' : 'primary'"
      :key="idx"
      v-for="({ hostBindings, containerPort, protocol }, idx) of ports"
    >
      {{ containerPort }}/{{ protocol.toLowerCase() }}
      <q-tooltip v-if="hostBindings.length">
        <div class="column ">
          <div
            class="col text-right"
            v-for="({ ip, port }, idx) of hostBindings"
            :key="idx"
          >
            {{ `${ip}:${port}` }}
          </div>
        </div>
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
