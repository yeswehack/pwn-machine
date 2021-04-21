<template>
  <q-badge :color="status ? 'positive' : 'negative'" class="q-ml-sm text-mono">
    {{ status ? "OK" : "ERROR" }}
  </q-badge>
</template>

<script>
export default {
  props: {
    status: { type: Boolean, required: true }
  }
};
</script>
