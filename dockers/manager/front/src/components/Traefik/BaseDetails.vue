<template>
  <div class="row q-col-gutter-md q-py-md">
    <div class="col-12" v-if="errors">
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
    errors: {
      type: Array
    }
  }
};
</script>
