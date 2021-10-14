<template>
  <div class="q-gutter-xs">
    <div class="row q-gutter-md items-center">
      <div class="col col-auto text-h6">Building {{ name }}</div>
      <div class="col">
        <q-badge :label="badgeLabel" :color="badgeColor" />
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <pre ref="logzone" class="scroll logzone">{{ logText }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import api from "src/api";

export default {
  props: {
    id: { type: String, required: true },
    name: { type: String, required: true },
  },
  data: () => ({ logText: "", done: false, error: false }),
  computed: {
    badgeColor () {
      if (this.error) {
        return "negative"
      }
      if (this.done) {
        return "positive"
      }
      return "warning"
    },
    badgeLabel () {
      if (this.error) {
        return "error"
      }
      if (this.done) {
        return "done"
      }
      return "running"
    }
  },
  apollo: {
    $subscribe: {
      dockerProgresBuild: {
        query: api.docker.streams.STREAM_BUILD,
        variables () {
          return { id: this.id };
        },
        result ({ data }) {
          const log = data.dockerStreamBuild;
          if (log.error) {
            this.error = true
            this.logText += `\n\n${log.error}`
          }
          if (log.stream) {
            this.logText += log.stream
            this.$nextTick(() => {
              this.$refs.logzone.scrollTo(0, this.$refs.logzone.scrollHeight)
            })
          }
          if (log.done) {
            this.done = true
            this.$emit("done")
          }
        }
      }
    }
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.logzone {
  max-height: 200px;
  margin: 0;
}
</style>