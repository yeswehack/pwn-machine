<template>
  <BaseTable
    ref="table"
    name="volume"
    rkey="Name"
    :expendable="true"
    :loading="loading"
    :data="volumes"
    :columns="columns"
  >
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-sm row">
        <ContainerLink :name="name" :key="name" v-for="[name] of usedBy(row)" />
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
import { mapGetters } from "vuex";
export default {
  components: { BaseTable, VolumeDetails, CreateVolume, ContainerLink },
  props: {
    containers: Array,
    images: Array,
    volumes: Array
  },
  computed: mapGetters(["loading"]),
  data() {
    return {
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "Name",
          sortable: true
        },
        {
          name: "path",
          label: "Path",
          align: "left",
          field: "Mountpoint",
          sortable: true
        },
        {
          name: "usedBy",
          label: "Used by",
          align: "left",
          field: row => this.usedBy(row),
          sortable: true
        }
      ]
    };
  },
  methods: {
    usedBy(row) {
      return this.containers
        .map(c => {
          const mounts = [];
          for (const mount of c.Mounts) {
            if (mount.Name != row.Name) continue;
            mounts.push([c.Name, mount.Destination]);
          }
          return mounts;
        })
        .filter(m => m.length)
        .flat();
    },
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
