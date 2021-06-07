<template>
  <div class="q-gutter-xs">
    <q-badge
      v-for="({ targets, containerPort, protocol }, idx) of ports"
      :key="idx"
      outline
      text-color="white"
      :style="{ 'border-color': targets ? 'var(--q-color-negative)' : 'black' }"
    >
      {{ containerPort }}/{{ protocol.toLowerCase() }}
      <q-tooltip v-if="targets" anchor="top middle" self="bottom middle">
        <div class="column ">
          <div
            v-for="(target, tidx) of targets || []"
            :key="`${idx}-${tidx}`"
            class="col text-right"
          >
            {{ `${target}` }}
          </div>
        </div>
      </q-tooltip>
    </q-badge>
    <q-badge v-if="host" title="host driver" color="positive" label="all" />
  </div>
</template>

<script>
export default {
  props: {
    ports: { type: Array, default: () => [] },
    host: { type: Boolean, default: false }
  }
};
</script>
