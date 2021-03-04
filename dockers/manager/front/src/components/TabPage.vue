<template>
  <q-page padding class="page">
    <q-tabs
      v-model="tab_"
      dense
      rounded
      inline-label
      shadow
      class="text-white bg-dark rounded-borders tabs"
      active-color="primary"
      indicator-color="primary"
      align="left"
      @input="updatePath"
      narrow-indicator
    >
      <slot name="top"></slot>
    </q-tabs>

    <q-tab-panels v-model="tab_" animated class="panels">
      <slot name="tabs"></slot>
    </q-tab-panels>
  </q-page>
</template>

<script>
export default {
  props: {
    tab: String,
    pathTemplate: String,
  },

  data() {
    return { tab_: this.tab };
  },
  methods: {
    updatePath(newVal) {
      if (newVal !== null)
        this.$router.push(this.pathTemplate.replace(/\{\}/, newVal));
    },
  },
  watch: {
    $route(to, from) {
      if (to.params.tab != this.tab_) {
        this.tab_ = to.params.tab;
      }
    },
  },
};
</script>
<style lang="scss" scoped>
/*
.q-page {
  display: flex;
  justify-content: stretch;
  flex-direction: row;
  flex-grow: 1;
  height: 100%;
}


.q-table {
  max-width: 100%;
}
.text-mono {
  font-family: monospace;
}
*/
.page .tabs {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.page {
  display: grid;
  grid-template-rows: auto 1fr;
  flex-direction: column;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14),
    0 3px 1px -2px rgba(0, 0, 0, 0.12);
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.refresh-btn {
  &.spin {
    animation: spin 1.5s linear 0s infinite;
  }
}
</style>