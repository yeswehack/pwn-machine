<template>
  <q-layout view="hhh lpR fFf" class="main-layout">
    <q-header class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title shrink class="q-mr-sm">
          <q-avatar class="q-mr-sm">
            <img src="/icons/logo.svg" class="logo" />
          </q-avatar>
          Pwn Machine
        </q-toolbar-title>

        <q-tabs v-if="showMenu" align="left" class="tabs col" narrow-indicator>
          <q-route-tab :to="{ name: 'dockerIndex' }" label="Docker" />
          <q-route-tab :to="{ name: 'dnsIndex' }" label="DNS" />
          <q-route-tab :to="{ name: 'traefikIndex' }" label="Traefik" />
          <q-route-tab :to="{ name: 'shellIndex' }" label="Shell" />
          <q-space />
          <q-route-tab :to="{ name: 'configIndex' }" label="Auth" />
        </q-tabs>
        <q-toolbar-title v-if="showMenu" shrink class="q-mr-sm">
          <q-btn flat round icon="logout" title="logout" @click="logout" />
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
    <Downloader />
    <Uploader />
    <stream-popup />
    <q-page-sticky class="refresh-btn" position="top-right" :offset="[16, 16]">
      <q-btn
        round
        color="primary"
        dense
        icon="refresh"
        :loading="loading"
        @click="refresh_"
      />
    </q-page-sticky>
  </q-layout>
</template>

<script>
import Downloader from "src/components/Downloader.vue";
import Uploader from "src/components/Uploader.vue";
import StreamPopup from "src/components/Docker/Streams/Popup.vue";

export default {
  name: "MainLayout",
  components: { Downloader, Uploader, StreamPopup },
  data: () => ({ loading: false }),
  computed: {
    showMenu() {
      return !this.$route.meta?.hideMenu;
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
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      window.location.reload();
    },
    async refresh_() {
      this.loading = true;
      window.setTimeout(() => (this.loading = false), 1000);
      this.refresh();
    }
  }
};
</script>

<style lang="scss" scoped>
.tabs a {
  text-decoration: none;
}
.main-layout {
  background-image: url("/icons/logo.svg");
  background-size: 50vh 50vh;
  background-repeat: no-repeat;
  background-position: 50% 50%;
}
</style>
