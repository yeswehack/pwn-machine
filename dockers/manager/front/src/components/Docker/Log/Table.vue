<template>
  <div class="docker-log-table ">
    <div class="row">
      <div class="col">
        <q-select
          v-model="selectedContainers"
          multiple
          use-chips
          clearable
          :options="containerOptions"
          filled
          label="Filter by container"
        />
      </div>
    </div>
    <log-list
      :key="selectedContainers ? selectedContainers.toString() : 'all'"
      :containers="selectedContainers"
    />
  </div>
</template>

<script>
import LogList from "src/components/Docker/Log/LogList.vue";
import api from "src/api";

export default {
  components: { LogList },
  data: () => ({ selectedContainers: [] }),
  apollo: {
    dockerContainers: {
      query: api.docker.containers.LIST_CONTAINERS
    }
  },
  computed: {
    containerOptions() {
      return (this.dockerContainers ?? []).map(c => c.name);
    }
  }
};
</script>

<style lang="scss" scoped>
.docker-log-table {
  width: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 14px;
  height: calc(100vh - 166px);
}
</style>
