<template>
  <base-table
    ref="table"
    name="image"
    row-key="id"
    :query="$apollo.queries.images"
    :data="images"
    :columns="columns"
    @delete="deleteImage"
  >
    <template #header-button>
      <q-btn
        rounded
        label="Prune"
        color="negative"
        icon="eva-trash-outline"
        @click="pruneImages"
      />
      <q-checkbox label="Show intermediate images" v-model="showIntermediate" />
    </template>
    <template #body-cell-images="{row}">
      <div class="q-gutter-sm row" style="max-width: 20vw">
        <image-link :name="name" :key="name" v-for="{ name } of row.usedBy" />
      </div>
    </template>

    <template #details> </template>sed
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import { format } from "quasar";
import ImageLink from "src/components/Docker/Image/Link.vue";
import api from "src/api";
const { humanStorageSize } = format;

export default {
  components: { BaseTable, ImageLink },
  apollo: {
    images: {
      query: api.docker.images.LIST_IMAGES,
      variables() {
        return { onlyFinal: !this.showIntermediate };
      },
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
      col("images", { label: "used by" })
    ];
    return { columns, showIntermediate: false };
  },
  methods: {
    deleteImage(image) {
      this.$api.docker.deleteImage(name.split("@")[0]);
      this.$emit("refetch");
    },
    pruneImages() {
      this.$q
        .dialog({
          title: "Prune images ?",
          message: "This will remove all dangling images.",
          color: "negative",
          options: {
            model: [],
            items: [
              {
                label:
                  "Also remove images without at least one container associated to them.",
                value: "full",

                color: "primary"
              }
            ],
            type: "toggle"
          },
          type: "confirm",
          cancel: true
        })
        .onOk(result => {
          const onlyDangling = !result.includes("full");
          const plural = (w, q) => (q > 1 ? w + "s" : s);
          this.$apollo
            .mutate({
              mutation: api.docker.images.PRUNE_IMAGES,
              variables: { onlyDangling },
              refetchQueries: [{ query: api.docker.images.LIST_IMAGES }]
            })
            .then(({ data }) => {
              const deleted = data.pruneDockerImages.deleted;
              const reclaimed = humanStorageSize(
                data.pruneDockerImages.spaceReclaimed
              );
              let message = `No image deleted.`;
              if (deleted.length) {
                message = `${deleted.length} ${plural(
                  "image",
                  deleted.length
                )} deleted (${reclaimed})`;
              }

              this.$q.notify({
                message,
                type: "positive"
              });
            });
        });
    }
  }
};
</script>
