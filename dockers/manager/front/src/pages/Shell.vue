<template>
  <tab-page>
    <q-route-tab
      :to="{ name: 'shellId', params: { uuid: nodeId } }"
      :name="nodeId"
      :key="nodeId"
      :label="containerName"
      v-for="{ nodeId, containerName } of shells"
    />
    <q-route-tab
      :to="{ name: 'shellNew' }"
      icon="add"
      class="bg-positive text-white"
    />
    <q-space />
  </tab-page>
</template>

<script>
import TabPage from "../components/TabPage.vue";
import gql from "src/api";

export default {
  components: { TabPage },
  apollo: {
    shells: {
      query: gql.docker.GET_CONTAINER_SHELLS,
      update: data => data.dockerContainerShells
    }
  }
};
</script>
