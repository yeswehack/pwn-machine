<template>
  <q-table
    dense
    :title="title"
    ref="table"
    class="edit-table"
    :pagination="pagination"
    :class="{ disabled: disable }"
    :columns="columnsWithDelete"
    :data="formData"
    hide-pagination
  >
    <template #body-cell="props">
      <q-td :props="props">
        {{ props.row[props.col.field] }}
        <q-popup-edit
          v-model="props.row[props.col.field]"
          v-if="!disable && !readonly"
        >
          <template #default="{value, emitValue, set}">
            <q-input
              :value="value"
              dense
              autofocus
              @input="emitValue"
              @keydown.tab="set"
            />
          </template>
        </q-popup-edit>
      </q-td>
    </template>
    <template #body-cell-delete="props">
      <q-td
        key="delete"
        :props="props"
        auto-width
        class="cursor-pointer"
        @click="deleteRow(props.row)"
      >
        &times;
      </q-td>
    </template>
    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="props"
    >
      <slot :name="slot" v-bind="{ ...props, disable, readonly }" />
    </template>

    <template #bottom v-if="!readonly">
      <div class="cursor-pointer text-center col col-grow" @click="addRow">
        +
      </div>
    </template>
    <template #no-data v-if="!readonly">
      <div class="cursor-pointer text-center col col-grow" @click="addRow">
        +
      </div>
    </template>
  </q-table>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  props: {
    title: String,
    columns: Array,
    value: Array,
    createDefault: {
      type: Function,
      default: () => () => ({})
    },
    disable: Boolean,
    readonly: Boolean,
    pagination: {
      type: Object,
      default: () => ({
        rowsPerPage: 0
      })
    }
  },
  computed: {
    columnsWithDelete() {
      if (this.readonly) {
        return this.columns;
      } else {
        return [
          ...this.columns,
          {
            name: "delete",
            label: "Remove",
            align: "center",
            format: () => "×"
          }
        ];
      }
    }
  },
  methods: {
    addRow() {
      if (this.disable) return;
      this.formData.push(this.createDefault());
    },
    deleteRow(row) {
      if (this.disable) return;
      this.formData = this.formData.filter(r => r != row);
    }
  }
};
</script>

<style lang="scss">
.edit-table .q-table__bottom {
  padding: 0;
  justify-items: stretch;
}
.edit-table:not(.disabled) .q-table__bottom div {
  line-height: 32px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  &:hover {
    background-color: $grey-8;
  }
}
</style>
