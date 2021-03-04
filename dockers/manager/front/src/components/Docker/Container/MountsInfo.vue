<template>
  <q-table
    title="Volumes"
    hide-pagination
    hide-no-data
    dense
    :pagination="pagination"
    :data="data"
    :columns="columns"
    row-key="name"
  >
    <template #body-cell-name="{ value }">
      <q-td><VolumeLink :name="value" v-if="value"/></q-td>
    </template>
  </q-table>
</template>

<script>
import VolumeLink from "src/components/Docker/Volume/Link.vue";
export default {
  components: { VolumeLink },
  props: {
    mounts: Array
  },
  data() {
    const columns = [
      {
        name: "name",
        align: "left",
        label: "Name",
        field: "Name"
      },
      {
        name: "destination",
        align: "left",
        label: "Mountpoint",
        field: "Destination"
      },
      {
        name: "source",
        align: "left",
        label: "Source",
        field: "Source"
      },
      {
        name: "mode",
        align: "left",
        label: "Mode",
        field: row => row.RW,
        format: v => (v ? "rw" : "ro")
      }
    ];

    const pagination = {
      rowsPerPage: 0
    };

    return { pagination, data: this.mounts, columns };
  }
};
</script>

<style></style>
