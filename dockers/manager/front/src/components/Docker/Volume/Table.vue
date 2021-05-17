<template>
  <base-table
    ref="table"
    name="volume"
    rkey="name"
    :expendable="true"
    :loading="loading"
    :data="volumes"
    :columns="columns"
  >
    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row">
        <container-link
          :name="name"
          :key="name"
          v-for="{ name } of row.containers"
        />
      </div>
    </template>
    <template #popup="{ info }">
      <create-volume :info="info" v-on:created="volumeCreated" />
    </template>
    <template #details="{ row }">
      <volume-details :name="row.Name" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import VolumeDetails from "src/components/Docker/Volume/Details.vue";
import CreateVolume from "src/components/Docker/Volume/Create.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";

export default {
  components: { BaseTable, VolumeDetails, CreateVolume, ContainerLink },
  apollo: {
    volumes: {
      query: api.docker.GET_VOLUMES,
      update: data => data.docker.volumes
    }
  },
  computed: {
    loading() {
      return this.$apollo.queries.getVolumes.loading;
    }
  },
  data() {
    const col = (name, opts = {}) => ({
      name,
      align: "left",
      label: name,
      field: name,
      sortable: true,
      ...opts
    });
    const columns = [
      col("name"),
      col("path", { field: "mountpoint" }),
      col("containers", {
        label: "used by",
        field: "usingContainers"
      })
    ];
    return { columns };
  },
  methods: {
    volumeCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    }
  }
};
</script>

<style lang="scss" scoped>
.short {
  max-width: 15vw;
}
</style>
