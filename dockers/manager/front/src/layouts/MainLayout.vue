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

      <q-tabs align="left" v-if="showMenu" class="tabs" narrow-indicator>
        <q-route-tab :to="{ name: 'dockerIndex' }" label="Docker" />
        <q-route-tab :to="{ name: 'dnsIndex' }" label="DNS" />
        <q-route-tab :to="{ name: 'traefikIndex' }" label="Traefik" />
        <q-route-tab :to="{ name: 'shellIndex' }" label="Shell" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
    <Downloader />
    <Uploader />
    <image-puller />
    <q-page-sticky class="refresh-btn" position="top-right" :offset="[16, 16]">
      <q-btn
        round
        color="primary"
        dense
        icon="refresh"
        @click="refresh_"
        :loading="loading"
      />
    </q-page-sticky>
  </q-layout>
</template>

<script>
import Downloader from "src/components/Downloader.vue";
import Uploader from "src/components/Uploader.vue";
import ImagePuller from "src/components/Docker/ImagePuller.vue";
export default {
  name: "MainLayout",
  components: { Downloader, Uploader, ImagePuller },
  computed: {
    showMenu() {
      return this.$route.name != "login";
    },
    requireLogin() {
      return false;
    }
  },
  data(){
    return {loading: false}
  },
  methods: {
    async refresh_() {
      this.loading = true;
      window.setTimeout(() => (this.loading = false), 1000);
      this.refresh();
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
