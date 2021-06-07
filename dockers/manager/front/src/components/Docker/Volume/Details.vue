<template>
  <div class="column q-py-sm">
    <div class="q-pa-md">
      <q-tree
        ref="tree"
        :nodes="files"
        :default-expand-all="true"
        :expanded.sync="expanded"
        :selected.sync="selected"
        node-key="fullpath"
        @lazy-load="onLazyLoad"
      >
        <template #header-folder="prop">
          <q-menu touch-position context-menu>
            <q-list dense class="rounded-borders ">
              <q-item v-close-popup clickable @click="uploadFile(prop.node)">
                <q-item-section avatar>
                  <q-avatar icon="backup" />
                </q-item-section>
                <q-item-section>
                  Upload in {{ prop.node.label }}
                </q-item-section>
              </q-item>
              <q-item
                v-close-popup
                clickable
                class="bg-negative"
                @click="deleteFile(prop.node)"
              >
                <q-item-section avatar>
                  <q-avatar icon="delete" />
                </q-item-section>
                <q-item-section>Delete "{{ prop.node.label }}"</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <div class="col">
            <q-icon
              :name="prop.expanded ? 'folder_open' : 'folder'"
              class="q-mr-sm"
            />
            {{ prop.node.label }}
          </div>
        </template>
        <template #header-file="prop">
          <q-menu touch-position context-menu>
            <q-list dense class="rounded-borders ">
              <q-item v-close-popup clickable @click="downloadFile(prop.node)">
                <q-item-section avatar>
                  <q-avatar icon="get_app" />
                </q-item-section>
                <q-item-section>
                  Download "{{ prop.node.label }}"
                </q-item-section>
              </q-item>
              <q-item
                v-close-popup
                clickable
                @click="uploadFile(getNode(prop.node.parent))"
              >
                <q-item-section avatar>
                  <q-avatar icon="backup" />
                </q-item-section>
                <q-item-section>
                  Upload in {{ getNode(prop.node.parent).label }}
                </q-item-section>
              </q-item>
              <q-item
                v-close-popup
                clickable
                class="bg-negative"
                @click="deleteFile(prop.node)"
              >
                <q-item-section avatar>
                  <q-avatar icon="delete" />
                </q-item-section>
                <q-item-section>Delete "{{ prop.node.label }}"</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <div class="col row q-gutter-md">
            <div class="col-auto text-right" style="width:50px">
              {{ prop.node.size }}
            </div>
            <div class="col">
              {{ prop.node.label }}
            </div>
          </div>
        </template>
      </q-tree>
    </div>

    <q-inner-loading :showing="loading">
      <q-spinner-gears size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import { DownloaderBus, UploaderBus } from "src/eventBus.js";
import { format } from "quasar";
import Vue from "vue";

export default {
  props: {
    name: { type: String, required: true }
  },
  data: () => ({
    files: [],
    loading: true,
    selected: [],
    expanded: [],
    splitterModel: 20,
    fileInfo: new Map()
  }),
  mounted() {
    this.fetchFiles().then(files => {
      const root = {
        header: "folder",
        icon: "folder",
        label: this.name,
        handler: this.toggleDir,
        fullpath: ""
      };
      root.children = this.parseFiles(files, root);
      this.files = [root];
      Vue.nextTick(() => this.$refs.tree.expandAll());

      this.loading = false;
    });
  },
  methods: {
    getNode(key) {
      return this.$refs.tree.getNodeByKey(key);
    },
    async fetchFiles(path = "") {
      return await this.$api.docker.getVolumeFiles(this.name, path);
    },

    async downloadFile(node) {
      const info = {
        volume: this.name,
        path: node.fullpath
      };
      await DownloaderBus.$emit("startDownload", info);
    },
    async uploadFile(node) {
      const info = {
        title: `Upload file(s) in ${node.label}`,
        url: this.$api.docker.getUploadLink(this.name, node.fullpath)
      };

      UploaderBus.$emit("startUpload", info);
    },
    async deleteFile(node) {
      await this.$api.docker.deleteFromVolume(this.name, node.fullpath);
      const parent = this.getNode(node.parent);
      parent.children = parent.children.filter(c => c !== node);
    },
    toggleDir(node) {
      this.$refs.tree.setExpanded(
        node.fullpath,
        !this.$refs.tree.isExpanded(node.fullpath)
      );
    },
    parseFiles(f, parent) {
      const folders = [];
      const files = [];
      for (const [name, file] of Object.entries(f)) {
        const fullpath = `${parent.fullpath}/${name}`;
        if (file.type === "DIR") {
          folders.push({
            lazy: true,
            handler: this.toggleDir,
            selectable: false,
            header: "folder",
            icon: "folder",
            parent: parent.fullpath,
            label: name,
            fullpath
          });
        }
        if (file.type === "REG") {
          files.push({
            label: name,
            header: "file",
            mime: file.mime[0],
            selectable: true,
            size: format.humanStorageSize(file.size),
            parent: parent.fullpath,
            fullpath
          });
        }
      }
      return folders.concat(files);
    },
    async onLazyLoad({ node, key, done, fail }) {
      const files = this.parseFiles(await this.fetchFiles(node.fullpath), node);
      done(files);
    }
  }
};
</script>
<style lang="scss" scoped>
.file {
  &:hover {
    background: red;
  }
}
</style>
