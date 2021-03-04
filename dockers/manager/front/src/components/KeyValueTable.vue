<template>
  <EditTable
    :title="title"
    :disable="disable"
    :readonly="readonly"
    :columns="columns"
    :createDefault="createPair"
    v-model="formData"
  />
</template>

<script>
import EditTable from "./EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: { EditTable },
  props: {
    disable: Boolean,
    title: String,
    labels: { type: Array, default: () => ["Name", "Value"] },
    readonly: Boolean
  },
  data() {
    const columns = [
      {
        name: "name",
        align: "left",
        label: this.labels[0],
        field: "name",
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

    const formData = Object.entries(this.value).map(([name, value]) => ({
      name,
      value
    }));
    return { columns, formData };
  },
  methods: {
    createPair() {
      return { name: "", value: "" };
    },
    renderFormData(v) {
      const obj = {};
      for (const { name, value } of v) {
        obj[name] = value;
      }
      return obj;
    }
  }
};
</script>
