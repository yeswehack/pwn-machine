<template>
  <q-table
    title="Connected containers"
    dense
    :pagination="pagination"
    hide-pagination
    :data="connectedContainers"
    :columns="connectedContainersColumns"
    row-key="name"
    no-data-label="No container connected"
  >
    <template #body-cell-name="props">
      <q-td> <ContainerLink :name="props.value" /> </q-td>
    </template>
    <template #bottoma-row>
      <q-tr>
        <q-td colspan="100%">
          <div>
            <q-btn color="positive" label="Attach a new container" />
          </div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import ContainerLink from "src/components/Docker/Container/Link.vue";
export default {
  components: { ContainerLink },
  props: {
    containers: Object
  },
  data() {
    const connectedContainers = Object.values(this.containers);
    const pagination = {
      rowsPerPage: 0
    };
    const connectedContainersColumns = [
      {
        name: "name",
        align: "left",
        label: "Name",
        field: "Name",
        sortable: true
      },
      {
        name: "ip",
        label: "IP",
        field: "IPv4Address",
        format: val => val.split("/")[0],
        sortable: true
      }
    ];
    return { connectedContainers, pagination, connectedContainersColumns };
  }
};
</script>

<style></style>
