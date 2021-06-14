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
          @finish="$root.refresh"
        />
      </q-card>
    </q-dialog>
  </q-slide-transition>
</template>

<script>
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
    UploaderBus.$on("startUpload", info => this.startUpload(info));
  },
  methods: {
    startUpload({ volume, path }) {
      const params = new URLSearchParams({ volume, path });
      this.url = `/file/upload?${params}`;
      this.title = `Upload in ${path}`;
      this.isOpen = true;
    }
  }
};
</script>
