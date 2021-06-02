<template>
  <tab-page :indicator-color="color">
    <q-route-tab
      :to="{ name: 'shellNew' }"
      icon="add"
      class="bg-positive text-white"
    />
    <q-route-tab
      :to="{ name: 'shellId', params: { id: nodeId } }"
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
      query: api.docker.shells.LIST_SHELLS,
      update: data => data.dockerContainerShells
    }
  },
  computed: {
    color() {
      return this.$route.name == "shellNew" ? "white" : "primary";
    }
  }
};
</script>
