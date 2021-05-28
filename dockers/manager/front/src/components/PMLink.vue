<template>
  <router-link :to="to" @click.native="$event.stopImmediatePropagation()">
    <q-badge class="col-auto" :color="color">
      {{ label }}
    </q-badge>
    <slot />
  </router-link>
</template>

<script>
export default {
  props: {
    path: { type: String, required: true },
    label: { type: String, required: true },
    hash: { type: String, default: null },
    color: { type: String, default: "primary" }
  },
  computed: {
    to() {
      return {
        path: this.path,
        hash: this.hash 
      };
    },
  }
};
</script>

<style></style>
