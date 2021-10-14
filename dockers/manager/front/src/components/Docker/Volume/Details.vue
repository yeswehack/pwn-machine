<template>
  <q-tree
    ref="tree"
    :nodes="files"
    :default-expand-all="true"
    :expanded.sync="expanded"
    :selected.sync="selected"
    node-key="fullpath"
    @lazy-load="onLazyLoad"
  >
    <template #header-folder="{node, expanded: isOpen}">
      <volume-menu :node="node" :volume-name="volume.name" />
      <div class="col">
        <q-icon :name="isOpen ? 'folder_open' : 'folder'" class="q-mr-sm" />
        {{ node.file.name }}
      </div>
    </template>
    <template #header-link="{node}">
      <volume-menu :node="node" :volume-name="volume.name" />
      <div class="col row q-gutter-md">
        <div class="col-auto text-right" style="width:50px">
          lnk
        </div>
        <div class="col">
          {{ node.file.name }} &rarr; {{ node.file.target }}
        </div>
      </div>
    </template>
    <template #header-file="{node}">
      <volume-menu :node="node" :volume-name="volume.name" />
      <div class="col row q-gutter-md">
        <div class="col-auto text-right" style="width:50px">
          {{ humanSize(node.file.size) }}
        </div>
        <div class="col">
          {{ node.file.name }}
        </div>
      </div>
    </template>
  </q-tree>
</template>

<script>
import { format } from "quasar";
import api from "src/api";
import VolumeMenu from "./VolumeMenu.vue";

export default {
  components: { VolumeMenu },
  props: {
    volume: { type: Object, required: true }
  },
  data: () => ({ files: [], selected: [], expanded: ["/"] }),
  mounted() {
    this.init();
  },
  methods: {
    async refresh() {
      await this.init();
      for (const path of this.expanded) {
        this.$refs.tree.setExpanded(path, true);
      }
    },
    async init() {
      const root = {
        header: "folder",
        file: {
          name: this.volume.name
        },
        handler: this.toggleDir,
        fullpath: "/"
      };
      root.children = await this.fetchAndParse("/", root);
      this.files = [root];
    },
    humanSize: s => format.humanStorageSize(s ?? 0),
    async fetchFiles(path = "") {
      const r = await this.$apollo.query({
        query: api.docker.volumes.EXPLORE_VOLUME,
        variables: { input: { volumeName: this.volume.name, path } },
        fetchPolicy: "network-only"
      });
      return r.data.dockerExploreVolume;
    },

    toggleDir(node) {
      const nodeIdx = this.expanded.indexOf(node.fullpath);
      if (nodeIdx < 0) {
        this.$refs.tree.setExpanded(node.fullpath, true);
      } else {
        this.$refs.tree.setExpanded(node.fullpath, false);
      }
    },
    parseFiles(f, parent) {
      const folders = [];
      const files = [];
      for (const file of f) {
        const node = {
          fullpath: file.fullpath,
          file,
          parent
        };

        switch (file.__typename) {
          case "DockerVolumeFolder":
            node.header = "folder";
            node.selectable = false;
            node.handler = this.toggleDir;
            node.lazy = true;

            folders.push(node);
            break;
          case "DockerVolumeLink":
            node.header = "link";
            files.push(node);
            break;
          default:
            node.header = "file";
            files.push(node);
            break;
        }
      }
      return folders.concat(files);
    },
    async fetchAndParse(path, parent) {
      const response = await this.fetchFiles(path);
      return this.parseFiles(response, parent);
    },
    async onLazyLoad({ node, key, done }) {
      done(await this.fetchAndParse(key, node));
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
