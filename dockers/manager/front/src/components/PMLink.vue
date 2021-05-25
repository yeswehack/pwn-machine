<template>
  <router-link :to="to"  @click.native="$event.stopImmediatePropagation()">
    <q-badge class="col-auto" :color="color">
      {{ shortName }}
    </q-badge>
    <slot />
  </router-link>
</template>

<script>
import { shortName } from "src/utils";
export default {
  props: {
    path: String,
    name: String,
    color: { type: String, default: "primary" }
  },
  computed: {
    to() {
      return {
        path: this.path,
        hash: this.name
      };
    },
    shortName() {
      return shortName(this.name);
    }
  }
};
</script>

<style></style>
