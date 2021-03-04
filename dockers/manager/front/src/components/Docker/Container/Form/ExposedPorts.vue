<template>
  <EditTable
    title="Exposed Ports"
    :disable="disable"
    dense
    :columns="columns"
    :createDefault="createPort"
    v-model="formData"
  >
    <template #body-cell-protocol="props">
      <q-td :props="props">
        <q-select
          :readonly="props.readonly"
          :disable="props.disable"
          :options="protocolOptions"
          v-model="props.row.protocol"
          dense
        />
      </q-td>
    </template>
  </EditTable>
</template>

<script>
import EditTable from "src/components/EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  components: { EditTable },
  mixins: [DeepForm],
  props: {
    value: Array,
    disable: Boolean
  },
  data() {
    const columns = [
      {
        name: "host",
        align: "left",
        label: "Host port",
        field: "host"
      },
      {
        name: "container",
        align: "left",
        label: "Container port",
        field: "container"
      },
      {
        name: "protocol",
        align: "left",
        label: "Protocol",
        field: "proto"
      }
    ];
    const protocolOptions = ["TCP", "UDP", "SCTP"];
    return { columns, protocolOptions };
  },
  methods: {
    createPort() {
      return { protocol: "TCP" };
    }
  }
};
</script>
