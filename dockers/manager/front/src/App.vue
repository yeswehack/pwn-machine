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
  data: () => ({ ready: false }),
  async created() {
    const token = localStorage.getItem("token");
    this.mutate({
      mutation: api.auth.REFRESH_TOKEN,
      variables: { token: token ?? "" }
    }).then(response => {
      if (response.isFirstRun) {
        if (this.$route.name !== "firstRun") {
          this.$router.push({ name: "firstRun" });
        }
      } else if (response.token) {
        localStorage.setItem("token", response.token);
      } else {
        if (this.$route.name !== "login") {
          this.$router.push({ name: "login" });
        }
      }
      this.ready = true;
    });
  }
};
</script>
