<template>
  <q-slide-transition>
    <q-card class="downloader" bordered v-show="downloading.length">
      <q-card-section
        class="q-py-none q-pl-sm"
        :key="idx"
        v-for="[idx, downloadInfo] of downloading.entries()"
      >
        <q-circular-progress
          size="50px"
          show-value
          instant-feedback
          :value="downloadInfo.progress"
          :color="downloadInfo.progress == 100 ? 'green' : 'lime'"
          class="q-ma-sm q-py-none"
        />
        {{ downloadInfo.name }}
      </q-card-section>
    </q-card>
  </q-slide-transition>
</template>

<script>
import { DownloaderBus } from "src/eventBus.js";
export default {
  created() {
    DownloaderBus.$on("startDownload", ({ volume, path }) => {
      this.downloadFile(volume, path);
    });
  },
  data() {
    return { value: 0, downloading: [] };
  },
  methods: {
    downloadBlob(blob, downloadInfo) {
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = downloadInfo.name;
      a.style.display = "none";
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => {
        this.downloading = this.downloading.filter(d => d != downloadInfo);
        URL.revokeObjectURL(url);
      });
    },

    async followProgress(reader, downloadInfo) {
      const chunks = [];
      let downloaded = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        downloaded += value.length;
        downloadInfo.progress = Math.floor(
          (downloaded / downloadInfo.size) * 100
        );
        chunks.push(value);
      }
      const blob = new Blob(chunks.flat(), {
        type: downloadInfo.mime
      });

      this.downloadBlob(blob, downloadInfo);
    },

    async downloadFile(volume, path) {
      const response = await this.$api.docker.downloadFromVolume(volume, path);

      const downloadInfo = {
        name: path.split("/").pop(),
        size: parseInt(response.headers.get("Content-Length")),
        mime: response.headers.get("Content-Type"),
        progress: 0,
        chunks: []
      };
      this.downloading.push(downloadInfo);
      const reader = response.body.getReader();
      this.followProgress(reader, downloadInfo);
    }
  }
};
</script>

<style lang="scss" scoped>
.downloader {
  position: fixed;
  bottom: 10px;
  right: 10px;
  z-index: 10000;
}
</style>
