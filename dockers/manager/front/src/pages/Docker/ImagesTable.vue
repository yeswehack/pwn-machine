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
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-sm row" style="max-width: 20vw">
        <ContainerLink
          :name="name"
          :key="name"
          v-for="{ name } of row.usedBy"
        />
      </div>
    </template>

    <template #details> </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
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
    return {
      columns: [
        {
          name: "id",
          label: "Image ID",
          align: "left",
          field: ({ id }) => id,
          classes: "text-mono",
          sortable: true
        },
        {
          name: "repository",
          align: "left",
          label: "Repository",
          field: ({ tags }) => tags[0]?.repository,
          sortable: true
        },
        {
          name: "tag",
          label: "Tag",
          align: "left",
          field: ({ tags }) => tags[0]?.tag,
          sortable: true
        },
        {
          name: "usedBy",
          label: "Used by",
          align: "left",
          field: "usedBy",
          sortable: true
        },
        {
          name: "createdAt",
          label: "Created",
          align: "left",
          field: "created",
          format: v => this.format_time(v),
          sortable: true
        },
        {
          name: "size",
          label: "Size",
          align: "left",
          field: "size",
          format: v => format.humanStorageSize(v),
          sortable: true
        }
      ]
    };
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
