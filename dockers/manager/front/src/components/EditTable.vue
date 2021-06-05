<template>
  <q-table
    dense
    ref="table"
    class="edit-table"
    :pagination="pagination"
    :class="{ disabled: disable }"
    :columns="columnsWithDelete"
    :data="formData"
    hide-pagination
    v-bind="$attrs"
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
      <q-td key="delete" :props="props" auto-width class="cursor-pointer">
        <q-btn
          icon="eva-close"
          round
          size="xs"
          @click="deleteRow(props.row)"
          color="negative"
        />
      </q-td>
    </template>
    <template
      v-for="slot in Object.keys($scopedSlots)"
      :slot="slot"
      slot-scope="props"
    >
      <slot :name="slot" v-bind="{ ...props, disable, readonly }" />
    </template>

    <template #bottom-row v-if="!readonly">
      <q-tr @click="addRow" class="cursor-pointer text-center">
        <q-td colspan="100%">
          <div class="q-py-sm">
            <q-btn flat size="xs" class="bg-positive" rounded icon="eva-plus" />
          </div>
        </q-td>
      </q-tr>
    </template>
    <template #bottom v-if="!readonly">
      <ResetAndSave :modified="modified" @save="submit" @reset="reset" />
    </template>
    <template #no-data v-if="!readonly">
      <ResetAndSave :modified="modified" @save="submit" @reset="reset" />
    </template>
  </q-table>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  props: {
    columns: Array,
    value: Array,
    createDefault: {
      type: Function,
      default: () => () => ({})
    },
    noButtons: { type: Boolean, default: false },
    disable: { type: Boolean, default: false },
    readonly: { type: Boolean, default: false },
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
            align: "center"
          }
        ];
      }
    },
    saveColor() {
      return this.modified ? "positive" : "grey";
    },
    resetColor() {
      return this.modified ? "primary" : "grey";
    }
  },
  methods: {
    submit() {
      this.$emit("submit");
    },
    addRow() {
      if (this.disable) return;
      this.formData = this.formData.concat([this.createDefault()]);
    },
    deleteRow(row) {
      if (this.disable) return;
      this.formData = this.formData.filter(r => r !== row);
    }
  }
};
</script>
