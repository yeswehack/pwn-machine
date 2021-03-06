<template>
  <q-table
    title="Connected containers"
    dense
    :pagination="pagination"
    hide-pagination
    :data="connected"
    :columns="columns"
    row-key="name"
    no-data-label="No container connected"
  >
    <template #body-cell-name="props">
      <q-td> <ContainerLink :name="props.value" /> </q-td>
    </template>
  </q-table>
</template>

<script>
import ContainerLink from "src/components/Docker/Container/Link.vue";
export default {
  components: { ContainerLink },
  props: {
    connected: Array
  },
  data() {
    const pagination = {
      rowsPerPage: 0
    };
    const columns = [
      {
        name: "name",
        align: "left",
        label: "Name",
        field: "name",
        sortable: true
      },
      {
        name: "ip",
        label: "IP",
        field: row => [row.ipv4, row.ipv6].filter(x => x).join(", "),
        format: val => val,
        sortable: true
      }
    ];
    return { pagination, columns };
  }
};
</script>

<style></style>
