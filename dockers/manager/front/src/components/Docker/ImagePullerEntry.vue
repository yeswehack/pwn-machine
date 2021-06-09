<template>
  <div class="q-gutter-xs">
    <div class="row q-gutter-md items-center">
      <div class="col col-auto text-h6">Pulling {{ pull.name }}</div>
      <div class="col">
        <q-badge
          :label="done ? 'done' : 'running'"
          :color="done ? 'positive' : 'warning'"
        />
      </div>
    </div>
    <div v-for="id of logIds" :key="id" class="row q-gutter-sm items-center">
      <div v-if="!id.startsWith('info-')" class="col col-auto">
        <span class="text-mono">{{ id }}</span>
      </div>
      <div
        v-if="lastLogs[id].progressDetail && lastLogs[id].progressDetail.total"
        class="col"
      >
        <q-linear-progress
          rounded
          size="4px"
          :value="
            lastLogs[id].progressDetail.current /
              lastLogs[id].progressDetail.total
          "
        />
      </div>
      <div
        v-else
        class="col ellipsis"
        style="max-width: 600px; overflow: hidden"
      >
        <span class="text-mono">{{ lastLogs[id].status }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import api from "src/api";
import Vue from "vue";

export default {
  props: {
    pull: { type: Object, required: true }
  },
  data: () => ({ logIds: [], lastLogs: {}, done: false }),
  apollo: {
    $subscribe: {
      pullImageProgress: {
        query: api.docker.images.PULL_IMAGE_SUBSCRIBE,
        variables() {
          return { id: this.pull.id };
        },
        result({ data }) {
          const log = data.pullImageProgress;
          if (!log) {
            this.done = true;
            this.pull.done?.();
            return;
          }
          const id = log.id ?? "info-" + Math.random().toString();
          if (!this.logIds.includes(id)) {
            this.logIds.push(id);
          }
          Vue.set(this.lastLogs, id, log);
        }
      }
    }
  },
  methods: {}
};
</script>
