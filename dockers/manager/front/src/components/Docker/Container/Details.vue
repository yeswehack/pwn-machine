<template>
  <div class="q-gutter-md q-py-sm">
    <div class="row">
      <q-card class="col">
        <q-card-section>
          <div class="row items-center">
            <div class="col-auto">
              <div class="text-h6">{{ container.name }}</div>
            </div>
            <div class="col-auto q-mx-md">
              <image-link :image="container.image" />
            </div>
            <div class="col-auto q-mx-md">
              <container-status :status="container.status" />
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
    <div class="row items-start">
      <div class="col q-mr-md">
        <q-card>
          <q-card-section>
            <div class="text-h6">
              Settings
            </div>
          </q-card-section>
          <create-container class="col" readonly :value="container" />
        </q-card>
      </div>
      <div class="col">
        <log-card>
          <log-list :containers="[container.name]" />
        </log-card>
      </div>
    </div>

    <details-process :processes="container.ps" v-if="container.ps" />
  </div>
</template>

<script>
import CreateContainer from "./Create.vue";
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import DetailsProcess from "./DetailsProcess.vue";
import api from "src/api";
import ShellDialog from "src/components/Shell/Dialog.vue";
import LogList from "src/components/Docker/Log/LogList.vue";
import LogCard from "src/components/LogCard.vue";

export default {
  components: {
    CreateContainer,
    DetailsProcess,
    LogCard,
    ImageLink,
    ContainerStatus,
    LogList
  },
  props: {
    container: { type: Object, required: true }
  },
  computed: {
    status() {
      switch (this.container.status.toLowerCase()) {
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
      this.$q.dialog({
        component: ShellDialog,
        parent: this,
        container: this.container
      }); /* 
      const uuid = await this.$api.shell.createContainerShell(
        this.container.Name
      );
      this.$router.push({ name: "shell", params: { tab: uuid } }); */
    },
    pauseContainer() {
      this.$apollo.mutate({
        mutation: api.docker.containers.PAUSE_CONTAINER,
        variables: { id: this.container.id },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
      });
    },
    async unpauseContainer() {
      this.$apollo.mutate({
        mutation: api.docker.containers.UNPAUSE_CONTAINER,
        variables: { id: this.container.id },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
      });
    },
    async startContainer() {
      this.$apollo.mutate({
        mutation: api.docker.containers.START_CONTAINER,
        variables: { id: this.container.id },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
      });
    },
    async stopContainer() {
      this.$apollo.mutate({
        mutation: api.docker.containers.STOP_CONTAINER,
        variables: { id: this.container.id },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
      });
    },
    async restartContainer() {
      this.$apollo.mutate({
        mutation: api.docker.containers.RESTART_CONTAINER,
        variables: { id: this.container.id },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
      });
    }
  }
};
</script>
