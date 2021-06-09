<template>
  <div class="row q-col-gutter-md q-py-md">
    <div v-if="errors && errors.length" class="col-12">
      <traefik-error :errors="errors" />
    </div>
    <slot name="body" />
  </div>
</template>

<script>
import TraefikError from "src/components/Traefik/TraefikError.vue";

export default {
  components: { TraefikError },
  props: {
    errors: { type: Array, default: () => [] }
  }
};
</script>
