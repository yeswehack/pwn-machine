<template>
    <BaseTable
      ref="table"
      name="image"
      :rkey="getTag"
      :loading="loading"
      :data="images"
      :columns="columns"
      v-on:delete="deleteContainer"
    >
      <template #body-cell-usedBy="{row}">
        <div class="q-gutter-sm row" style="max-width: 20vw">
          <ContainerLink :name="name" :key="name" v-for="name of usedBy(row)" />
        </div>
      </template>

      <template #details> </template>
    </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import { format } from "quasar";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import { mapGetters } from "vuex";

export default {
  components: { BaseTable, ContainerLink },
  
  props: {
    containers: Array,
    //images: Array
  },
  data() {
    return {
      columns: [
        {
          name: "repository",
          align: "left",
          label: "Repository",
          field: "Repository",
          sortable: true
        },
        {
          name: "tag",
          label: "Tag",
          align: "left",
          field: "Tag",
          sortable: true
        },
        {
          name: "id",
          label: "Image ID",
          align: "left",
          field: "Id",
          style: "font-family: monospace",
          format: v => this.shortId(v),
          sortable: true
        },
        {
          name: "usedBy",
          label: "Used by",
          align: "left",
          field: row => this.usedBy(row),
          sortable: true
        },
        {
          name: "createdAt",
          label: "Created",
          align: "left",
          field: "Created",
          format: v => this.format_time(v),
          sortable: true
        },
        {
          name: "size",
          label: "Size",
          align: "left",
          field: "Size",
          format: v => format.humanStorageSize(v),
          sortable: true
        }
      ]
    };
  },
  computed: mapGetters(["loading"]),
  methods: {
    getTag(row) {
      return `${row.Repository}:${row.Tag}`;
    },
    usedBy(row) {
      const tag = this.getTag(row);
      return this.containers
        .filter(c => {
          const image = c.Config.Image;
          return image.indexOf(":") > 0
            ? image == tag
            : `${image}:latest` == tag;
        })
        .map(c => c.Name);
    },
    shortId(id) {
      return id.substr(7, 12);
    },
    getStatusColor(status) {
      switch (status) {
        case "running":
        case "created":
        case "restarting":
          return "positive";
        case "paused":
          return "primary";
        case "removing":
        case "exited":
          return "orange";
        case "dead":
          return "negative";
      }
      return "primary";
    },
    humanSize(s) {
      return humanSize(s);
    },
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
