<template>
  <q-slide-transition>
    <q-dialog v-model="isOpen">
      <q-card>
        <q-uploader
          ref="uploader"
          no-thumbnails
          :url="url"
          :label="title"
          multiple
          :headers="headers"
          auto-upload
        />
      </q-card>
    </q-dialog>
  </q-slide-transition>
</template>

<script>
import Vue from "vue";
import { UploaderBus } from "src/eventBus.js";

export default {
  props: {},
  data: () => ({ isOpen: false, url: null, title: "Upload" }),
  computed: {
    headers: () => [
      {
        name: "Authorization",
        value: `Bearer ${localStorage.getItem("token")}`
      }
    ]
  },
  created() {
    UploaderBus.$on("startUpload", ({ title, url }) => {
      this.startUpload(title, url);
    });
  },
  methods: {
    startUpload(title, url) {
      this.title = title;
      this.url = url;
      this.isOpen = true;
      Vue.nextTick(() => {
        this.$refs.uploader.pickFiles();
      });
    }
  }
};
</script>
