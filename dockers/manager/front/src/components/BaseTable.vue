<template>
  <q-table
    v-on="$listeners"
    v-bind="$attrs"
    hide-pagination
    ref="table"
    class="full-width"
    table-header-style="text-transform: capitalize"
    :row-key="rowKey"
    :loading="loading"
    :columns="columns"
    :pagination="pagination"
    :filter="filter"
    :no-data-label="`You don't have any ${name}.`"
    :expanded.sync="expanded"
    @row-click="toggleRow"
  >
    <template #top>
      <div class="row full-width justify-between">
        <div class="col q-gutter-md">
          <q-btn
            rounded
            color="positive"
            icon="eva-plus"
            :label="txt.create"
            @click="$emit('create')"
            :disable="noNew"
          />
          <slot name="header-button" />
        </div>

        <div class="col col-auto">
          <q-input
            borderless
            label="Search"
            dense
            outlined
            debounce="200"
            v-model="filter"
          >
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
        </div>
      </div>
    </template>
    <template #body="props">
      <q-tr
        class="base-row"
        :props="props"
        :name="props.row[rowKey]"
        @click="toggleRow(props.row)"
      >
        <q-menu touch-position context-menu v-if="!noMenu">
          <q-list dense class="rounded-borders bg-grey-9">
            <slot name="menu" v-bind="{ row: props.row }" />
            <q-item v-close-popup clickable @click="$emit('clone', props.row)">
              <q-item-section avatar>
                <q-avatar icon="eva-copy" />
              </q-item-section>
              <q-item-section>{{ txt.clone }}</q-item-section>
            </q-item>
            <q-item
              v-close-popup
              clickable
              class="bg-negative"
              @click="$emit('delete', props.row)"
            >
              <q-item-section avatar>
                <q-avatar icon="eva-trash" />
              </q-item-section>
              <q-item-section>{{ txt.delete }}</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
        <q-td
          v-for="col in props.cols"
          :key="col.name"
          :props="props"
          :auto-width="col.autoWidth"
        >
          <slot
            :name="`body-cell-${col.name}`"
            v-bind="{ ...props, value: col.value }"
          >
            {{ col.value }}
          </slot>
        </q-td>
      </q-tr>
      <template v-if="!$props.noDetails">
        <q-tr
          v-if="props.expand"
          :props="props"
          no-hover
          class="expand  bg-grey-10"
        >
          <q-td colspan="100%">
            <slot name="details" v-bind="{ row: props.row }"></slot>
          </q-td>
        </q-tr>
      </template>
    </template>

    <template #no-data="props">
      <q-btn
        round
        flat
        size="xs"
        icon="eva-loader-outline"
        :loading="loading"
        class=" q-mr-md no-pointer-events"
      />
      {{ props.message }}
    </template>
  </q-table>
</template>

<script>
export default {
  props: {
    "no-details": { type: Boolean, default: false },
    "no-new": { type: Boolean, default: false },
    "no-menu": { type: Boolean, default: false },
    query: { type: Object, required: true },
    rowKey: { type: String, default: "nodeId" },
    name: { type: String },
    columns: Array
  },
  data() {
    return {
      row: null,
      filter: "",
      pagination: {
        sortBy: this.columns[0].name,
        rowsPerPage: 0
      },
      txt: {
        create: `New ${this.name}`,
        clone: `Clone ${this.name}`,
        delete: `Delete ${this.name}`
      },
      expanded: this.$router.hash ? this.$router.hash.split(",") : []
    };
  },
  computed: {
    loading() {
      return this.query.loading;
    },
    bodySlots() {
      return this.columns.map(k => `body-cell-${k.name}`);
    }
  },
  mounted() {
    if (this.$route.hash) {
      const expanded = this.$route.hash.slice(1).split(",");
      if (!expanded.length) return;
      this.expanded = expanded;
      const last = this.expanded[this.expanded.length - 1];
      window.setTimeout(() => {
        const el = document.querySelector(`.base-row[name='${last}']`);
        if (!el) return;
        el.scrollIntoView(true, { behavior: "smooth" });
      }, 500);
    }
  },
  methods: {
    toggleRow(row) {
      const name = row[this.rowKey];
      const idx = this.expanded.indexOf(name);
      if (idx == -1) {
        this.expanded.push(name);
      } else {
        this.expanded.splice(idx, 1);
      }
      this.$router.replace({ hash: this.expanded.join(",") });
      this.$refs.table.setExpanded(this.expanded);
    }
  }
};
</script>
