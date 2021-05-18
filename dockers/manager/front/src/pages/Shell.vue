<template>
  <tab-page>
    <q-route-tab
      :to="{ name: 'shellNew' }"
      icon="add"
      class="bg-positive text-white"
    />
    <q-route-tab
      :to="{ name: 'shellId', params: { uuid: nodeId } }"
      :name="nodeId"
      :key="nodeId"
      :label="containerName"
      v-for="{ nodeId, containerName } of shells"
    />
  </tab-page>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import api from "src/api";

export default {
  components: { TabPage },
  apollo: {
    shells: {
      query: api.docker.GET_CONTAINER_SHELLS,
      update: data => data.dockerContainerShells
    }
  }
};
</script>
