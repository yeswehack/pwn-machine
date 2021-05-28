<template>
  <q-badge
    :label="status ? 'OK' : 'ERROR'"
    :color="status ? 'positive' : 'negative'"
    class="q-ml-sm text-mono"
  />
</template>

<script>
export default {
  props: {
    status: { type: Boolean, required: true }
  }
};
</script>
