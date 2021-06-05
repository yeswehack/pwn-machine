<template>
  <EditTable
    title="Networks"
    :disable="disable"
    :columns="columns"
    :createDefault="createRow"
    v-model="formData"
  >
    <template #body-cell-name="props">
      <q-td :props="props">
        <q-select
          :options="networkNames"
          v-model="props.row.name"
          :disable="disable"
          @filter="filter"
          input-debounce="0"
          dense
          use-input
        />
      </q-td>
    </template>
    <template #body-cell-aliases="props">
      <q-td :props="props">
        <q-select
          v-model="props.row.aliases"
          use-input
          use-chips
          dense
          multiple
          hide-dropdown-icon
          input-debounce="0"
          new-value-mode="add-unique"
        />
      </q-td>
    </template>
  </EditTable>
</template>

<script>
import EditTable from "src/components/EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";

export default {
  mixins: [DeepForm],
  components: { EditTable },
  props: {
    value: Array,
    disable: Boolean
  },
  data() {
    const columns = [
      {
        name: "name",
        align: "left",
        label: "Name",
        field: "name"
      },
      {
        name: "aliases",
        align: "left",
        label: "Aliases",
        field: "Aliases"
      }
    ];
    return { columns, test: null, test2: null };
  },
  computed: {
    networkNames() {
      return this.$store.getters["docker/networks"]
        .filter(network => network.Driver === "bridge")
        .map(network => network.Name);
    }
  },
  methods: {
    filter(val, update) {
      update(() => {
        if (val === "") {
          this.options = this.networkNames;
        } else {
          const needle = val.toLowerCase();
          this.options = this.networkNames.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          );
        }
      });
    },
    createRow() {
      return { name: null, aliases: this.getDefaultAliases() };
    },
    getDefaultAliases() {
      if (this.formData.length > 0) {
        return this.formData[this.formData.length - 1].aliases;
      }
      return [];
    }
  }
};
</script>
