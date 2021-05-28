<template>
  <pm-link path="/docker/images" :hash="image.shortId" :label="image.name" />
</template>

<script>
import PmLink from "src/components/PMLink.vue";
export default {
  components: { PmLink },
  props: { image: { type: Object, required: true } },
};
</script>
