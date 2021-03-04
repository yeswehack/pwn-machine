<template>
  <EditTable
    :columns="columns"
    :createDefault="createVolume"
    v-model="formData"
  >
    <template #body-cell-type="props">
      <q-td>
        <q-select
          dense
          :options="['volume', 'bind', 'tmpfs']"
          v-model="props.row.type"
        />
      </q-td>
    </template>
    <template #body-cell-name="props">
      <q-td>
        <q-select
          dense
          :options="volumeNames"
          v-model="props.row.name"
          v-if="props.row.type == 'volume'"
        />
        <template v-else-if="props.row.type == 'bind'">
          {{ props.row.name }}
          <q-popup-edit v-model="props.row.name">
            <q-input v-model="props.row.name" dense autofocus />
          </q-popup-edit>
        </template>
        <div v-else class="disabled text-center">n/a</div>
      </q-td>
    </template>
    <template #body-cell-mode="props">
      <q-td auto-width><q-toggle dense size="sm" v-model="props.row.rw"/></q-td>
    </template>
  </EditTable>
</template>

<script>
import { shortName } from "src/utils";
import EditTable from "src/components/EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: { EditTable },
  props: {
    mounts: Array
  },
  data() {
    const columns = [
      {
        name: "type",
        align: "left",
        label: "Type",
        field: "type"
      },
      {
        name: "name",
        align: "left",
        label: "name / source",
        field: "name"
      },
      {
        name: "destination",
        align: "left",
        label: "Destination",
        field: "destination"
      },
      {
        name: "mode",
        align: "left",
        label: "RW",
        field: row => row.rw,
        format: v => (v ? "rw" : "ro")
      }
    ];

    const pagination = {
      rowsPerPage: 0
    };

    return {
      pagination,
      columns
    };
  },
  methods: {
    createVolume() {
      return {
        type: "volume",
        name: null,
        rw: true,
        destination: null
      };
    }
  },
  computed: {
    volumeNames() {
      return this.$store.getters["docker/volumes"].map(v => shortName(v.Name));
    }
  }
};
</script>
