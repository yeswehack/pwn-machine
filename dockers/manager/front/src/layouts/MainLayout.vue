<template>
  <q-layout view="hhh lpR fFf">
    <q-header class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo/svg/quasar-logo.svg" />
          </q-avatar>
          Pwn Machine
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left" v-if="showMenu" class="tabs">
        <q-route-tab :to="{ name: 'dockerIndex' }" label="Docker" />
        <q-route-tab :to="{ name: 'dnsIndex' }" label="DNS" />
        <q-route-tab :to="{ name: 'traefikIndex' }" label="Traefik" />
        <q-route-tab :to="{ name: 'shellIndex' }" label="Shell" />
        <q-space />
        <q-route-tab :to="{ name: 'index' }" label="Config" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <transition>
        <router-view />
      </transition>
    </q-page-container>
    <Downloader />
    <Uploader />
  </q-layout>
</template>

<script>
import Downloader from "src/components/Downloader.vue";
import Uploader from "src/components/Uploader.vue";
export default {
  name: "MainLayout",
  components: { Downloader, Uploader },
  computed: {
    showMenu() {
      return this.$route.name != "login";
    },
    requireLogin() {
      return false;
    }
  },
  watch: {
    requireLogin(v) {
      if (v) {
        this.$router.push({ name: "login" });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.tabs a {
  text-decoration: none;
}
</style>