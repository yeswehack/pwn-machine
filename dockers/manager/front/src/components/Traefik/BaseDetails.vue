<template>
  <div class="row q-col-gutter-md q-py-md items-stretch justify-evenly">
    <div class="col-12" v-if="errors">
      <TraefikError :errors="errors" />
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
