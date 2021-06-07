<template>
  <div class="overview">
    <div ref="graphContainer" class="graph-container"></div>
    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
export default {
  props: {
    loading: { type: Boolean, default: false }
  },
  methods: {
    getContainer() {
      return this.$refs.graphContainer;
    }
  }
};
</script>

<style lang="scss" scoped>
.graph-container {
  width: 100%;
  height: calc(100% - 20px);
}
.overview {
  height: 100%;
  width: 100%;
}
</style>
