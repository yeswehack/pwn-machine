<template>
  <base-table
    ref="table"
    name="image"
    row-key="id"
    :query="$apollo.queries.images"
    :data="images"
    :columns="columns"
    v-on:delete="deleteContainer"
  >
    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row" style="max-width: 20vw">
        <container-link
          :name="name"
          :key="name"
          v-for="{ name } of row.usingContainers"
        />
      </div>
    </template>

    <template #details> </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import { format } from "quasar";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";

export default {
  components: { BaseTable, ContainerLink },
  apollo: {
    images: {
      query: api.docker.images.LIST_IMAGES,
      variables: { onlyFinal: true },
      update: ({ dockerImages }) => dockerImages
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
      col("created"),
      col("size", { format: v => format.humanStorageSize(v) }),
      col("containers", { label: "used by" })
    ];
    return { columns };
  },
  methods: {
    format_time(s) {
      if (!s) return "";
      const dtFormat = new Intl.DateTimeFormat("default", {
        dateStyle: "short",
        timeStyle: "medium",
        hour12: false
      });

      return dtFormat.format(new Date(s));
    },
    containerCreated() {
      this.$emit("refetch");
      this.$refs.table.closePopup();
    },
    deleteContainer(name) {
      this.$api.docker.deleteContainer(name.split("@")[0]);
      this.$emit("refetch");
    }
  }
};
</script>
