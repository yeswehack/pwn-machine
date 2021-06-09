<template>
  <base-table
    ref="table"
    name="image"
    row-key="shortId"
    :query="$apollo.queries.images"
    :data="images"
    :columns="columns"
    @create="createImage"
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
      <q-checkbox v-model="showIntermediate" label="Show intermediate images" />
    </template>
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-sm row" style="max-width: 20vw">
        <container-link
          v-for="{ name } of row.usedBy"
          :key="name"
          :name="name"
        />
      </div>
    </template>
    <template #body-cell-shortId="{row}">
      <div class="text-mono">{{ row.shortId }}</div>
    </template>
    <template #body-cell-tags="{row}">
      <div class="row q-gutter-sm">
        <div
          v-for="tag of row.tags"
          :key="`${row.shortId}-${tag}`"
          class="col col-auto"
        >
          <q-badge
            dense
            class="q-px-sm"
            outline
            style="border-color:var(--q-color-primary)"
          >
            {{ tag }}
          </q-badge>
        </div>
      </div>
    </template>

    <template #details="{row}">
      <image-details :image="row" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import { format } from "quasar";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";
import ImageSearchVue from "../Container/Form/ImageSearch.vue";
import ImageDetails from "./Details.vue";
const { humanStorageSize } = format;

export default {
  components: { BaseTable, ContainerLink, ImageDetails },
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
      col("shortId", { label: "Id", autoWidth: true }),
      col("tags"),
      col("usedBy", { label: "used by" }),
      col("created", { autoWidth: true }),
      col("size", { format: v => format.humanStorageSize(v), autoWidth: true })
    ];
    return { columns, showIntermediate: false };
  },
  methods: {
    deleteImage(image) {
      this.$q
        .dialog({
          title: "Confirm",
          options: {
            model: [],
            items: [
              {
                label: "Do not delete untagged parents",
                value: "noPruneParents",

                color: "primary"
              }
            ],
            type: "toggle"
          },
          message: `Are you sure you want to delete ${image.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(result => {
          const pruneParent = !result.includes("noPruneParents");
          this.mutate({
            mutation: api.docker.images.DELETE_IMAGE,
            variables: { id: image.id, force: true, pruneParent },
            refetchQueries: [{ query: api.docker.images.LIST_IMAGES }],
            message: `${image.name} deleted.`
          });
        });
    },
    createImage() {
      this.$q
        .dialog({
          component: ImageSearchVue,
          parent: this
        })
        .onOk(tag => {
          this.$refs.select.add(tag);
          this.form = tag;
        });
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
          this.mutate({
            mutation: api.docker.images.PRUNE_IMAGES,
            variables: { onlyDangling },
            refetchQueries: [{ query: api.docker.images.LIST_IMAGES }]
          }).then(result => {
            const deleted = result.deleted;
            const reclaimed = humanStorageSize(result.spaceReclaimed);
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
