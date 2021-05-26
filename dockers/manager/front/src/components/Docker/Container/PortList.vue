<template>
  <div class="q-gutter-xs">
    <q-badge
      :color="targets ? 'negative' : 'grey-9'"
      :key="idx"
      v-for="({ targets, containerPort, protocol }, idx) of ports"
    >
      {{ containerPort }}/{{ protocol.toLowerCase() }}
      <q-tooltip
        v-if="targets"
        anchor="top middle"
        self="bottom middle"
      >
        <div class="column ">
          <div
            class="col text-right"
            v-for="(target, idx) of targets"
            :key="idx"
          >
            {{ `${target}` }}
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
    ports: { type: Array, default: () => [] },
    host: { type: Boolean, default: false }
  }
};
</script>

<style></style>
