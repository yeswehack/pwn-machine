<template>
  <BaseTable
    ref="table"
    name="volume"
    rkey="name"
    :expendable="true"
    :loading="loading"
    :data="volumes"
    :columns="columns"
  >
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-sm row">
        <ContainerLink
          :name="name"
          :key="name"
          v-for="{ name } of row.usedBy"
        />
      </div>
    </template>
    <template #popup="{ info }">
      <CreateVolume :info="info" v-on:created="volumeCreated" />
    </template>
    <template #details="{ row }">
      <VolumeDetails :name="row.Name"></VolumeDetails>
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import VolumeDetails from "src/components/Docker/Volume/Details.vue";
import CreateVolume from "src/components/Docker/Volume/Create.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import gql from "src/gql";

export default {
  components: { BaseTable, VolumeDetails, CreateVolume, ContainerLink },
  apollo: {
    volumes: {
      query: gql.docker.GET_VOLUMES,
      update: data => data.docker.volumes
    }
  },
  computed: {
    loading() {
      return this.$apollo.queries.getVolumes.loading;
    }
  },
  data() {
    return {
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "name",
          sortable: true
        },
        {
          name: "path",
          label: "Path",
          align: "left",
          field: "mountpoint",
          sortable: true
        },
        {
          name: "usedBy",
          label: "Used by",
          align: "left",
          field: row => row.usedBy.map(c => c.name),
          sortable: true
        }
      ]
    };
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
