<template>
  <BaseTable
    ref="table"
    name="image"
    rkey="id"
    :loading="loading"
    :data="images"
    :columns="columns"
    v-on:delete="deleteContainer"
  >
    <template #body-cell-containers="{row}">
      <div class="q-gutter-sm row" style="max-width: 20vw">
        <ContainerLink
          :name="name"
          :key="name"
          v-for="{ name } of row.containers"
        />
      </div>
    </template>

    <template #details> </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable3.vue";
import { format } from "quasar";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import gql from "src/gql";

export default {
  components: { BaseTable, ContainerLink },
  apollo: {
    images: {
      query: gql.docker.GET_IMAGES,
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
      col("name", { format: v => v ?? "<no name>" }),
      col("created"),
      col("size", { format: format.humanStorageSize }),
      col("containers", {
        label: "used by",
        field: "usingContainers"
      })
    ];
    return { columns };
  },
  computed: {
    loading() {
      return this.$apollo.queries.images.loading;
    }
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
