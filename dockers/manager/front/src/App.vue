<template>
  <div id="q-app">
    <router-view />
  </div>
</template>
<script>
import { Dark } from "quasar";

Dark.set(true);

export default {
  name: "App",
};

</script>
<style lang="scss">
</style>
