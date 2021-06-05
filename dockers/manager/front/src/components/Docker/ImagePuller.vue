<template>
  <q-page-sticky :offset="[16, 16]">
    <transition appear leave-active-class="animated fadeOut slower">
      <q-card v-show="visible" style="width: 500px">
        <transition-group
          tag="div"
          appear
          leave-active-class="animated fadeIn fadeOut delay-3s"
        >
          <q-card-section
            :key="`${pull.name}-${idx}`"
            v-for="(pull, idx) of pulls"
            v-show="!pull.over"
          >
            <image-puller-entry :pull="pull" @close="pull.over = true" />
          </q-card-section>
        </transition-group>
      </q-card>
    </transition>
  </q-page-sticky>
</template>

<script>
import api from "src/api";
import ImagePullerEntry from "./ImagePullerEntry.vue";
import { PullImageBus } from "src/eventBus.js";

export default {
  components: { ImagePullerEntry },
  data: () => ({ pulls: [] }),
  computed: {
    visible() {
      return this.pulls.some(pull => !pull.over);
    }
  },
  methods: {
    async pullImage(name, done) {
      this.mutate({
        mutation: api.docker.images.PULL_IMAGE,
        variables: { name }
      }).then(result => {
        const { id } = result.pullDockerImage;
        const pull = { id, name, over: false };
        pull.done = () => {
          pull.over = false;
          window.setTimeout(() => {
            const pos = this.pulls.findIndex(p => p === pull);
            this.pulls.splice(pos, 1);
          }, 3000);
          done();
        };
        this.pulls.push(pull);
      });
    }
  },
  created() {
    PullImageBus.$on("pullImage", ({ name, done }) => {
      this.pullImage(name, done);
    });
  },
  destroyed() {
    PullImageBus.$off("pullImage");
  }
};
</script>
