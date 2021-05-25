<template>
  <div class="scroll thin-scrollbar" >
    <q-infinite-scroll
      style="max-width: 0px"
      :offset="200"
      @load="onLoad"
      reverse
    >
      <div class="docker-log-list">
        <template v-for="(log, idx) of items">
          <div class="text-mono text-no-wrap" :key="`${idx}-date`">
            {{ formatDate(log.date) }}
          </div>
          <div
            class="text-mono text-no-wrap"
            :key="`${idx}-name`"
            :style="{ color: colorHash.hex(log.containerName) }"
          >
            {{ log.containerName }}
          </div>
          <div
            :key="`${idx}-msg`"
            class="text-mono text-no-wrap"
            v-html="toHtml(log.message)"
          />
        </template>
      </div>
      <template v-slot:loading>
        <div class="row justify-center q-my-md">
          <q-spinner-dots color="primary" size="40px" />
        </div>
      </template>
    </q-infinite-scroll>
  </div>
</template>

<script>
import api from "src/api";
import { date } from "quasar";
import ansiToHtml from "ansi-to-html";
import ColorHash from "color-hash";

const ansiColorConverter = new ansiToHtml();

export default {
  props: {
    containers: { type: Array, default: () => [] },
    rowsPerPage: { type: Number, default: 50 },
    short: { type: Boolean, default: false }
  },
  apollo: {
    dockerLogs: {
      query: api.docker.logs.LIST_LOGS,
      variables() {
        return {
          filter: { containerName: [] },
          cursor: { from: 0, size: this.rowsPerPage }
        };
      },
      update: data => {
        return data.dockerLogs.result;
      },
      fetchPolicy: "network-only"
    }
  },
  methods: {
    onLoad(index, done) {
      console.log(index);
      this.$apollo.queries.dockerLogs.fetchMore({
        variables: {
          filter: { containerName: this.containers },
          cursor: {
            from: (index - 1) * this.rowsPerPage,
            size: this.rowsPerPage
          }
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          const logs = fetchMoreResult.dockerLogs.result;
          this.items.splice(0, 0, ...logs.reverse());
          done(logs.length == 0);
        }
      });
    },
    formatDate(s) {
      return date.formatDate(s, "MM-DD HH:mm:ss");
    },
    toHtml(s) {
      // escape bell 0x07
      if (s.includes("\x07")) {
        s = s.split("\x07")[1];
      }
      const r = ansiColorConverter.toHtml(s, { newLine: true, stream: true });
      return r;
    },
    refresh() {
      this.items.splice(0, this.items.length);
      this.onLoad(1, x => x);
    }
  },
  watch: {
    containers(v) {
      this.refresh();
    }
  },
  data() {
    const colorHash = new ColorHash({ lightness: 0.7, saturation: 1 });
    return { items: [], colorHash };
  },
  mounted() {
      const parent = this.$parent.$el
      const rowHeight = 28;
      const headerHeight = parent.firstElementChild ? parent.firstElementChild.getBoundingClientRect().height : 0
      const padding = headerHeight + rowHeight + rowHeight + 10; // search + header + lastrow in px
      const height = parent.getBoundingClientRect().height;
      this.pagination.rowsPerPage = Math.floor((height - padding) / rowHeight);
  },
  computed: {
    logs() {
      return this.dockerLogs ?? [];
    }
  }
};
</script>

<style lang="scss">
.docker-log-list {
  display: grid;
  grid-template-columns: auto  auto 1fr;
  column-gap: 10px;
}
</style>
