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
                  @click="openShell"
                />
                <q-btn
                  :loading="btnLoad.pause"
                  round
                  color="primary"
                  icon="pause"
                  title="Pause the container"
                  @click="pressButton('pause')"
                />
                <q-btn
                  :loading="btnLoad.restart"
                  round
                  color="orange"
                  icon="replay"
                  title="Restart the container"
                  @click="pressButton('restart')"
                />
                <q-btn
                  :loading="btnLoad.stop"
                  round
                  color="negative"
                  icon="stop"
                  title="Stop the container"
                  @click="pressButton('stop')"
                />
              </template>
              <template v-else-if="status == 'paused'">
                <q-btn
                  :loading="btnLoad.unpause"
                  round
                  color="primary"
                  icon="play_arrow"
                  title="Unpause the container"
                  @click="pressButton('unpause')"
                />
                <q-btn
                  :loading="btnLoad.restart"
                  round
                  color="orange"
                  icon="replay"
                  title="restart the container"
                  @click="pressButton('restart')"
                />
                <q-btn
                  :loading="btnLoad.stop"
                  round
                  color="negative"
                  icon="stop"
                  title="Stop the container"
                  @click="pressButton('stop')"
                />
              </template>
              <template v-else>
                <q-btn
                  :loading="btnLoad.start"
                  round
                  color="positive"
                  icon="play_arrow"
                  title="Start the container"
                  @click="pressButton('start')"
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
  data() {
    const btnLoad = {
      start: false,
      restart: false,
      stop: false,
      pause: false,
      unpause: false
    };
    return { btnLoad };
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
      });
    },
    pressButton(name) {
      const mutations = {
        start: api.docker.containers.START_CONTAINER,
        restart: api.docker.containers.RESTART_CONTAINER,
        stop: api.docker.containers.STOP_CONTAINER,
        pause: api.docker.containers.PAUSE_CONTAINER,
        unpause: api.docker.containers.UNPAUSE_CONTAINER
      };
      this.btnLoad[name] = true;
      this.$apollo
        .mutate({
          mutation: mutations[name],
          variables: { id: this.container.id },
          refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
        })
        .catch(e => {
          this.$q.notify({
            message: e.message,
            type: "negative"
          });
        })
        .finally(() => {
          this.btnLoad[name] = false;
        });
    },
  }
};
</script>
