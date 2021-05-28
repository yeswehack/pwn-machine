<template>
  <base-dialog ref="dialog" title="Search image" class="searchImage">
    <q-card-section>
          <q-input
            filled
            clearable
            label="Search"
            class="full-width"
            v-model="search"
            @input="doSearch"
          />
    </q-card-section>
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="image">
        <q-table
          flat
          style="max-height: 50vh"
          :columns="imageColumns"
          :data="imageSearchResults || []"
          :loading="$apollo.loading"
          virtual-scroll
          row-key="name"
          :rows-per-page-options="[0]"
          @row-click="selectImage"
        >
          <template #body-cell-name="props">
            <q-td :props="props">
              {{ props.value }}
              <q-tooltip>
                {{ props.row.description }}
              </q-tooltip>
            </q-td>
          </template>
          <template #body-cell-link="props">
            <q-td :props="props">
              <q-btn
                flat
                round
                type="a"
                :href="dockerLink(props.row)"
                target="_blank"
                rel="noopener noreferrer"
                icon="info"
                size="sm"
                @click.stop=""
              />
            </q-td>
          </template>
          <template #body-cell-isOfficial="props">
            <q-td :props="props" auto-width>
              <q-icon
                :name="props.value ? 'check' : 'close'"
                :color="props.value ? 'positive' : 'negative'"
              />
            </q-td>
          </template>
          <template #body-cell-starCount="props">
            <q-td :props="props" auto-width>
              <div class="row q-gutter-xs justify-end align-center">
                <span class="col">{{
                  props.value > 10000
                    ? (props.value / 1000).toFixed(0) + "K"
                    : props.value
                }}</span>
                <div class="col col-auto">
                  <q-icon color="yellow" name="star" />
                </div>
              </div>
            </q-td>
          </template>
        </q-table>
      </q-tab-panel>

      <q-tab-panel name="tag">
        <q-table
          flat
          style="max-height: 50vh"
          :columns="tagColumns"
          :data="tagsSeachResults || []"
          :loading="$apollo.loading"
          virtual-scroll
          row-key="name"
          :rows-per-page-options="[0]"
        >
          <template #body-cell-pull="{row}">
            <q-td align="right">
              <div v-if="isAvailable(row)">
                <q-btn
                  label="update"
                  class="q-px-sm"
                  color="positive"
                  :loading="!!loadings[row.name]"
                  dense
                  @click="pullImage(row.name)"
                />
              </div>
              <div v-else>
                <q-btn
                  label="pull"
                  class="q-px-sm"
                  color="primary"
                  :loading="!!loadings[row.name]"
                  dense
                  @click="pullImage(row.name)"
                />
              </div>
            </q-td>
          </template>
        </q-table>
      </q-tab-panel>
    </q-tab-panels>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import api from "src/api";
import { PullImageBus } from "src/eventBus.js";
import { format } from "quasar";
import Vue from "vue";
export default {
  components: { BaseDialog },
  apollo: {
    imageSearchResults: {
      query: api.docker.images.SEARCH_IMAGE,
      debounce: 250,
      throttle: 250,
      skip() {
        return !Boolean(this.search);
      },
      variables() {
        return { search: this.search };
      },
      update: data => data.dockerSearchImage,
      fetchPolicy: "cache-first"
    },
    tagsSeachResults: {
      query: api.docker.images.SEARCH_IMAGE_TAG,
      skip: true,
      update: data => data.dockerSearchImageTag,
      variables() {
        const partition = (s, needle) => {
          const pos = s.indexOf(needle);
          if (pos < 0) {
            return ["", s];
          }
          return [s.slice(0, pos), s.slice(pos + needle.length)];
        };
        const [repoName, imageName] = partition(this.search, "/");
        return { imageName, repoName: repoName || "library" };
      },
      fetchPolicy: "cache-first"
    },
    dockerImages: {
      query: api.docker.images.LIST_IMAGES,
      update: data => new Set(data.dockerImages.map(i => i.name))
    }
  },
  data() {
    const col = (name, opts = {}) => ({
      name,
      label: name,
      field: name,
      sortable: true,
      ...opts
    });
    const imageColumns = [
      col("name", { label: "Name", align: "left" }),
      col("link", { label: "Link", align: "center" }),
      col("isOfficial", { label: "Official", align: "center" }),
      col("starCount", { label: "Stars" })
    ];

    const tagColumns = [
      col("name", { align: "left" }),
      col("size", { label: "Size", format: v => format.humanStorageSize(v) }),
      col("pull", { label: "" })
    ];

    return {
      imageColumns,
      tagColumns,
      search: null,
      selected: [],
      panel: "image",
      loadings: {}
    };
  },
  methods: {
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    isAvailable(tag) {
      return this.dockerImages.has(tag.name);
    },
    selectImage(evt, row) {
      this.search = row.name;
      this.$apollo.queries.tagsSeachResults.skip = false;
      this.panel = "tag";
    },
    pullImage(name) {
      Vue.set(this.loadings, name, true);
      console.log("fire", { name });
      PullImageBus.$emit("pullImage", {
        name,
        done: () => {
          Vue.set(this.loadings, name, false);
          this.$apollo.queries.dockerImages.refetch();
        }
      });
    },
    dockerLink(image) {
      if (image.isOfficial) {
        return `https://hub.docker.com/_/${image.name}`;
      }
      return `https://hub.docker.com/r/${image.name}`;
    },
    doSearch(search) {
      this.panel = "image";
      this.$apollo.queries.tagsSeachResults.skip = true;
    }
  }
};
</script>

<style lang="scss">
.searchImage {
  & thead tr th {
    position: sticky;
    z-index: 1;
    background: #1d1d1d;
  }

  & thead tr:last-child th {
    /* height of all previous header rows */
    top: 48px;
  }
  & thead tr:first-child th {
    top: 0;
  }
}
</style>
