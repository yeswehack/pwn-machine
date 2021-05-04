<template>
  <div class="column q-py-sm">
    <template v-if="!loading">
      <div class="col col-grow q-mb-md">
        <q-card dark class="bg-dark">
          <q-card-section class="q-pa-md">
            <div class="row justify-between items-center">
              <div class="col-auto">
                <div class="text-h6">{{ name }}</div>
              </div>
              <div class="col-auto q-mx-md">
                <ImageLink :name="container.image.repository" />
              </div>
              <div class="col-auto q-mx-md">
                <ContainerStatus :status="container.status" />
              </div>
              <q-space />
              <div class="col-auto q-gutter-sm">
                <template v-if="status == 'running'">
                  <q-btn
                    round
                    color="grey"
                    icon="navigate_next"
                    title="Open a shell in the container"
                    @click="openShell()"
                  />
                  <q-btn
                    round
                    color="primary"
                    icon="pause"
                    title="Pause the container"
                    @click="pauseContainer()"
                  />
                  <q-btn
                    round
                    color="orange"
                    icon="replay"
                    title="Restart the container"
                    @click="restartContainer()"
                  />
                  <q-btn
                    round
                    color="negative"
                    icon="stop"
                    title="Stop the container"
                    @click="stopContainer()"
                  />
                </template>
                <template v-else-if="status == 'paused'">
                  <q-btn
                    round
                    color="primary"
                    icon="play_arrow"
                    title="Unpause the container"
                    @click="unpauseContainer()"
                  />
                  <q-btn
                    round
                    color="orange"
                    icon="replay"
                    title="restart the container"
                    @click="restartContainer()"
                  />
                  <q-btn
                    round
                    color="negative"
                    icon="stop"
                    title="Stop the container"
                    @click="stopContainer()"
                  />
                </template>
                <template v-else>
                  <q-btn
                    round
                    color="positive"
                    icon="play_arrow"
                    title="Start the container"
                    @click="startContainer()"
                  />
                </template>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
      <div class="row q-col-gutter-md">
        <!-- NETWORKS -->
        <div class="col col-grow" v-if="0">
          <NetworksInfo :settings="container.connectedNetworks" />
        </div>
        <!-- ENVIRON -->
        <div class="col col-grow">
          <KeyValueTable title="Environ" readonly :value="container.environ" />
        </div>
        <!-- LABELS -->
        <div class="col col-grow">
          <KeyValueTable title="Labels" readonly :value="container.labels" />
        </div>

        <!-- VOLUMES -->
        <div class="col col-grow" v-if="container.mounts.length">
          <MountsInfo :mounts="container.mounts" />
        </div>

        <!-- LOGS -->
        <div class="col col-12" v-if="0">
          <q-card dark class="bg-dark">
            <q-card-section>
              <div class="text-h6">Logs</div>
            </q-card-section>

            <q-separator dark inset />
            <q-card-section class="q-pa-md">
              <q-scroll-area horizontal style="height: 200px">
                <pre>{{ container.Logs }}</pre>
              </q-scroll-area>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </template>

    <q-inner-loading :showing="loading">
      <div class="row q-col-gutter-md">
        <q-spinner-gears size="50px" color="primary" />
      </div>
    </q-inner-loading>
  </div>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";
import NetworksInfo from "src/components/Docker/Container/NetworksInfo.vue";
import MountsInfo from "src/components/Docker/Container/MountsInfo.vue";
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import gql from "src/gql";

export default {
  components: {
    KeyValueTable,
    NetworksInfo,
    MountsInfo,
    ImageLink,
    ContainerStatus
  },
  props: {
    name: {
      type: String,
      required: true
    }
  },
  apollo: {
    container: {
      query: gql.docker.GET_CONTAINERS,
      variables() {
        return { name: this.name };
      },
      update: ({ container }) => container
    }
  },
  data() {
    return {};
  },
  computed: {
    loading() {
      return this.$apollo.queries.container.loading;
    },
    status() {
      switch (this.container.status) {
        case "running":
        case "restarting":
          return "running";
        case "paused":
          return "paused";
        case "created":
        case "removing":
        case "exited":
        case "dead":
        default:
          return "dead";
      }
    }
  },
  methods: {
    async openShell() {
      const uuid = await this.$api.shell.createContainerShell(
        this.container.Name
      );
      this.$router.push({ name: "shell", params: { tab: uuid } });
    },
    pauseContainer() {
      this.$store.dispatch("docker/pauseContainer", this.container.Name);
    },
    async unpauseContainer() {
      this.$store.dispatch("docker/unpauseContainer", this.container.Name);
    },
    async startContainer() {
      this.$api.docker.startContainer(this.container.Name);
    },
    async stopContainer() {
      this.$api.docker.stopContainer(this.container.Name);
    },
    async restartContainer() {
      this.$api.docker.restartContainer(this.container.Name);
    }
  }
};
</script>

<style lang="scss" scoped>
.logs {
  position: relative;
  width: 100px;
}
pre {
  width: 100%;
  overflow: auto;
  word-break: break-word;
}
.details > * {
  min-width: 300px;
}
.q-card {
  height: 100%;
  overflow: auto;
  scrollbar-width: thin;
}
code:not(:empty) {
  background: var(--q-color-dark);
  padding: 1px 5px;
  border-radius: 4px;
  white-space: nowrap;
}
</style>
