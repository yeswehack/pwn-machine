<template>
  <base-table
    name="volume"
    row-key="name"
    :expendable="true"
    :loading="$apollo.queries.volumes.loading"
    :data="volumes"
    :columns="columns"
    no-details
  >
    <template #body-cell-usingContainers="{row}">
      <div class="q-gutter-sm row">
        <container-link
          :name="name"
          :key="name"
          v-for="{ name } of row.usingContainers"
        />
      </div>
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";

export default {
  components: { BaseTable, ContainerLink },
  apollo: {
    volumes: {
      query: api.docker.GET_VOLUMES,
      update: data => data.dockerVolumes
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
      col("usingContainers", {
        label: "used by",
        field: "usingContainers"
      })
    ];
    return { columns };
  },
};
</script>
