<template>
  <div class="log-card bg-dark">
    <div class="text-h6 title">
      Logs
    </div>
    <slot name="default" />
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.log-card {
  height: 400px;
  overflow: hidden;
  display: grid;
  grid-template-rows: auto 1fr;
  border-radius: 4px;
  padding: 16px;
  row-gap: 16px;
}
</style>
