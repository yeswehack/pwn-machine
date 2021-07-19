<template>
  <q-page-sticky :offset="[16, 16]">
    <q-card v-show="visible" style="width: 500px">
      <q-card-section v-for="(pull, idx) of pulls" :key="`${pull.name}-${idx}`">
        <pull-entry :id="pull.id" :name="pull.name" @done="pull.done" />
      </q-card-section>
      <q-card-section
        v-for="(build, idx) of builds"
        :key="`${build.name}-${idx}`"
      >
        <build-entry :id="build.id" :name="build.name" @done="build.done" />
      </q-card-section>
    </q-card>
  </q-page-sticky>
</template>

<script>
import api from "src/api";
import PullEntry from "./PullEntry.vue";
import BuildEntry from './BuildEntry.vue';
import { GlobalBus } from 'src/eventBus';

export default {
  components: { PullEntry, BuildEntry },
  apollo: {
    dockerStreams: {
      query: api.docker.streams.LIST_STREAMS,
      update (data) {
        data.dockerStreams.forEach(meta => {
          if (meta.type == "PULL") {
            this.followPull(meta)
          }
          if (meta.type == "BUILD") {
            this.followBuild(meta)
          }
        })
      }
    },
  },
  data: () => ({ pulls: [], builds: [] }),
  computed: {
    visible () {
      return [...this.pulls, ...this.builds].length;
    }
  },
  created () {
    GlobalBus.$on("pullDockerImage", this.pullDockerImage)
    GlobalBus.$on("buildDockerImage", this.buildDockerImage)
  },
  destroyed () {
    GlobalBus.$off("pullDockerImage", this.pullDockerImage)
    GlobalBus.$off("buildDockerImage", this.buildDockerImage)
  },
  methods: {
    async pullDockerImage ({ name, done }) {
      this.mutate({
        mutation: api.docker.images.PULL_IMAGE,
        variables: { name }
      }).then(async meta => {
        await this.followPull(meta)
        done()
      })
    },
    async buildDockerImage ({ tag, url, done }) {
      this.mutate({
        mutation: api.docker.images.BUILD_IMAGE,
        variables: { input: { tag, url } }
      }).then(async meta => {
        await this.followBuild(meta)
        done()
      })
    },
    followPull (meta) {
      return new Promise(resolve => {
        const pull = { id: meta.id, name: meta.name };
        pull.done = () => {
          GlobalBus.$emit("refetchDockerImages")
          window.setTimeout(() => {
            const pos = this.pulls.findIndex(p => p === pull);
            this.pulls.splice(pos, 1);
          }, 3000);
          resolve()
        };
        this.pulls.push(pull)
      })
    },
    followBuild (meta) {
      return new Promise(resolve => {
        const build = { id: meta.id, name: meta.name };
        this.builds.push(build)
        build.done = () => {
          resolve()
          GlobalBus.$emit("refetchDockerImages")

          window.setTimeout(() => {
            const pos = this.builds.findIndex(p => p === build);
            this.builds.splice(pos, 1);
          }, 3000);
        };
      })
    },
  }
};
</script>
