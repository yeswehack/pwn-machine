<template>
  <EditTable
    :title="title"
    :disable="disable"
    :readonly="readonly"
    :columns="columns"
    :createDefault="createPair"
    v-model="formData"
    v-bind="$attrs"
  />
</template>

<script>
import EditTable from "./EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: { EditTable },
  props: {
    disable: { type: Boolean, default: false },
    title: {type: String, default: ""},
    labels: { type: Array, default: () => ["Name", "Value"] },
    readonly: { type: Boolean, default: false }
  },
  data() {
    const columns = [
      {
        name: "name",
        align: "left",
        label: this.labels[0],
        field: "key",
        headerStyle: "width: 50%"
      },
      {
        name: "value",
        align: "left",
        label: this.labels[1],
        headerStyle: "width: 50%",
        field: "value"
      }
    ];

    const formData = this.value;
    return { columns, formData };
  },
  methods: {
    createPair() {
      return { key: "", value: "" };
    }
  }
};
</script>
