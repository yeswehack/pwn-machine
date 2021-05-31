<template>
  <a class="text-white" :href="href" target="_blank" title="Help" @click.stop>
    <q-icon size="sm" name="eva-question-mark-circle" />
  </a>
</template>

<script>
export default {
  props: {
    href: { type: String, required: true }
  },
};
</script>

<style></style>
