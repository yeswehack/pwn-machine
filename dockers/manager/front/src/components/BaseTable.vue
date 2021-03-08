<template>
  <div>
    <q-table
      ref="table"
      :data="data"
      :columns="columns"
      :loading="loading"
      :filter="filter"
      :pagination="pagination"
      :row-key="rkey"
      class="pm-table"
      hide-pagination
      :no-data-label="`You don't have any ${name}.`"
      flat
      @update:expanded="updateHash"
      :expanded.sync="expanded"
    >
      <template #top>
        <q-btn
          rounded
          color="positive"
          icon="add"
          :label="txt.create"
          @click="newRow"
        />
        <q-space />
        <q-input borderless dense outlined debounce="200" v-model="filter">
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template #body="props">
        <q-tr
          :props="props"
          :name="getName(props.row)"
          @click="toggleRow(props.row)"
        >
          <q-menu touch-position context-menu>
            <q-list class="rounded-borders bg-grey-9">
              <q-item v-close-popup clickable @click="cloneRow(props.row)">
                <q-item-section avatar>
                  <q-avatar style="font-size: 2em" icon="file_copy" />
                </q-item-section>
                <q-item-section>{{ txt.clone }}</q-item-section>
              </q-item>
              <q-item
                v-close-popup
                clickable
                class="bg-negative"
                @click="deleteRow(getName(props.row))"
              >
                <q-item-section avatar>
                  <q-avatar style="font-size: 2em" icon="delete" />
                </q-item-section>
                <q-item-section>{{ txt.delete }}</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <template v-if="`body-cell-${col.name}` in $scopedSlots">
              <slot :name="`body-cell-${col.name}`" v-bind="props" />
            </template>
            <template v-else>
              {{ col.value }}
            </template>
          </q-td>
        </q-tr>

        <q-tr v-if="props.expand" :props="props" no-hover class="expand">
          <q-td colspan="100%">
            <slot name="details" v-bind:row="props.row"></slot>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    <q-dialog v-model="popupVisible">
      <slot name="popup" v-bind:info="popupInfo"></slot>
    </q-dialog>
  </div>
</template>

<script>
import Vue from "vue";
export default {
  components: {},
  props: {
    expendable: { type: Boolean, default: true },
    data: Array,
    name: String,
    clone: { type: Function, default: () => () => null },
    columns: Array,
    rkey: [String, Function],
    loading: Boolean,
  },
  data() {
    return {
      filter: "",
      pagination: {
        rowsPerPage: 0
      },
      popupInfo: null,
      txt: {
        create: `New ${this.name}`,
        clone: `Clone ${this.name}`,
        delete: `Delete ${this.name}`
      },
      popupVisible: false,
      expanded: this.$router.hash ? this.$router.hash.split(",") : []
    };
  },
  mounted() {
    if (this.$route.hash) {
      this.showRows(this.$route.hash.substr(1), true);
    }
  },
  watch: {
    $route(to, from) {
      // dont scroll when closing
      const scroll = to.path == from.path && to.hash.length > from.hash.length;
      this.showRows(this.$route.hash.substr(1), scroll);
    }
  },
  methods: {
    toggleRow(row) {
      const name = this.getName(row);
      const idx = this.expanded.indexOf(name);
      if (idx == -1) {
        this.expanded.push(name);
      } else {
        this.expanded.splice(idx, 1);
      }
      this.$refs.table.setExpanded(this.expanded);
    },
    getName(row) {
      if (typeof this.rkey === "string") return row[this.rkey];
      return this.rkey(row);
    },

    // Url hash handlers
    showRows(names, scroll) {
      if (names) {
        names = names.split(",");
        this.$refs.table.setExpanded(names);
        const lastOpen = names[names.length - 1];
        if (!scroll) {
          return;
        }
        const row = document.querySelector(`.q-tr[name='${lastOpen}']`);
        if (row) {
          Vue.nextTick(() =>
            row.scrollIntoView({ behavior: "smooth", block: "start" })
          );
        }
      }
    },
    updateHash(names) {
      const hash = `#${names.join(",")}`;
      if (hash != this.$route.hash) {
        this.$router.replace({ hash });
      }
    },
    // Row handlers
    newRow() {
      this.popupInfo = null;
      this.$emit("newRow");
      this.popupVisible = true;
    },
    cloneRow(row) {
      this.popupInfo = row;

      this.$emit("cloneRow", row);
      this.popupVisible = true;
    },
    deleteRow(name) {
      this.$emit("delete", name);
    },
    closePopup() {
      this.popupVisible = false;
    }
  }
};
</script>

<style lang="scss">
.expand {
  background-color: #3d3d3d;
}
</style>
