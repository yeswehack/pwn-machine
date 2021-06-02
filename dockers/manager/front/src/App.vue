<template>
  <div id="q-app">
    <router-view v-if="ready" />
  </div>
</template>
<script>
import { Dark } from "quasar";
import api from "./api";

Dark.set(true);

export default {
  name: "App",
  data() {
    return { ready: false };
  },
  async created() {
    const token = localStorage.getItem("token");
    const r = await this.$apollo.mutate({
      mutation: api.auth.VALIDATE_TOKEN,
      variables: { token: token ?? "" }
    });
    const response = r.data.validateAuthToken;
    if (response.isFirstRun) {
      if (this.$route.name != "firstRun") {
        this.$router.push({ name: "firstRun" });
      }
    } else if (response.token) {
      localStorage.setItem("token", response.token.token);
    } else {
      if (this.$route.name != "login") {
        this.$router.push({ name: "login" });
      }
    }
    this.ready = true
  }
};
</script>
<style lang="scss"></style>
