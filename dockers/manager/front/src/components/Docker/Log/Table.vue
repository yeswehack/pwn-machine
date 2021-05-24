<template>
  <div class="full-width column q-gutter-md">
    <div class="col col-auto full-width">
      <div class="row">
        <div class="col">
          <q-select
            multiple
            use-chips
            clearable
            v-model="selectedContainers"
            :options="containerOptions"
            filled
            label="Filter by container"
          />
        </div>
      </div>
    </div>
    <div class="col full-width">
      <log-list :key="selectedContainers.toString()" :containers="selectedContainers"/>
    </div>
  </div>
</template>

<script>
import LogList from "src/components/Docker/LogList.vue";
import api from "src/api";
export default {
  components: { LogList },
  data() {
    return { selectedContainers: [] };
  },
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

<style></style>
