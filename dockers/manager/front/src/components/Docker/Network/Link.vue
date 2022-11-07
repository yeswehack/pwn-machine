<template>
  <div>
    <div v-if="network.deleted">
      <q-badge
        text-color="white"
        outline
        class="deleted"
        :label="network.name"
      />

      <q-tooltip anchor="top middle" self="bottom middle">
        Deleted
      </q-tooltip>
    </div>
    <pm-link
      v-else
      path="/docker/networks"
      :hash="network.name"
      :label="network.name"
    >
      <slot />
    </pm-link>
  </div>
</template>

<script>
import PmLink from "src/components/PMLink.vue";

export default {
  components: { PmLink },
  props: {
    network: { type: Object, required: true }
  }
};
</script>
<style lang="scss" scoped>
.deleted {
  border-color: var(--q-color-negative);
}
</style>
