<template>
  <a class="text-white" :href="href" target="_blank">
    <q-icon size="sm" name="help" />
  </a>
</template>

<script>
export default {
  props: {
    href: String
  }
};
</script>

<style></style>
