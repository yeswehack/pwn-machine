<template>
  <q-menu touch-position context-menu>
    <q-list dense class="rounded-borders ">
      <q-item v-close-popup clickable @click="uploadFile">
        <q-item-section avatar>
          <q-avatar icon="backup" />
        </q-item-section>
        <q-item-section> Upload in {{ folderPath }} </q-item-section>
      </q-item>
      <q-item
        v-if="node.header == 'file'"
        v-close-popup
        clickable
        @click="downloadFile"
      >
        <q-item-section avatar>
          <q-avatar icon="download" />
        </q-item-section>
        <q-item-section> Download {{ file.fullpath }} </q-item-section>
      </q-item>
      <q-item v-close-popup clickable class="bg-negative" @click="deleteFile">
        <q-item-section avatar>
          <q-avatar icon="delete" />
        </q-item-section>
        <q-item-section>Delete "{{ file.name }}"</q-item-section>
      </q-item>
    </q-list>
  </q-menu>
</template>

<script>
import { DownloaderBus, UploaderBus } from "src/eventBus.js";
import api from "src/api";
export default {
  props: {
    volumeName: { type: String, required: true },
    node: { type: Object, required: true }
  },
  computed: {
    file() {
      return this.node.file;
    },
    folderPath() {
      return this.node.header == "folder"
        ? this.node.fullpath
        : this.node.parent.fullpath;
    }
  },
  methods: {
    async downloadFile() {
      const info = {
        volume: this.volumeName,
        path: this.node.fullpath,
        file: this.node.file
      };
      await DownloaderBus.$emit("startDownload", info);
    },
    async uploadFile() {
      const info = {
        volume: this.volumeName,
        path: this.folderPath
      };

      UploaderBus.$emit("startUpload", info);
    },
    async deleteFile() {
      const input = {
        volumeName: this.volumeName,
        path: this.node.fullpath
      };

      this.$q
        .dialog({
          type: "confirm",
          title: "Confirm",
          message: `Are you sure you want to delete ${input.path}?`,
          cancel: true,
          ok: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.volumes.DELETE_FILE,
            variables: { input }
          }).then(() => {
            this.$root.refresh();
          });
        });
    }
  }
};
</script>

<style></style>
