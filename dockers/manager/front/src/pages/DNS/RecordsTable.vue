<template>
  <BaseTable
    ref="table"
    name="record"
    :rkey="r => r.zone + r.name + r.type + r.record"
    :loading="loading"
    :data="records"
    :columns="columns"
  >
    <template #body-cell-zone="{row}">
      <div class="q-gutter-sm row">
        <ZoneLink :name="row.zone" />
      </div>
    </template>
    <template #body-cell-enabled="{row}">
      <q-toggle v-model="row.enabled" color="green" />
    </template>
    <template #popup>
      <CreateRecord v-model="recordForm" v-on:submit="createRecord" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "../../components/BaseTable.vue";
import ZoneLink from "src/components/DNS/Zone/Link.vue";
import CreateRecord from "src/components/DNS/Record/Create.vue";
import { mapGetters } from "vuex";
export default {
  components: { BaseTable, ZoneLink, CreateRecord },
  props: {
    zones: Array,
    records: Array
  },
  methods: {
    createRecord() {}
  },
  computed: {
    ...mapGetters(["loading"]),
  },
  data() {
    const recordForm = {
      zone: "",
      type: "",
      record: "",
      enable: true,
    };
    return {
      recordForm,
      columns: [
        {
          name: "zone",
          align: "left",
          label: "Zone",
          field: row => row.zone,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "name",
          label: "Name",
          align: "left",
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: "type",
          label: "Type",
          align: "left",
          field: row => row.type,
          sortable: true
        },
        {
          name: "content",
          label: "Content",
          align: "left",
          field: row => row.content,
          sortable: true
        },
        {
          name: "ttl",
          label: "TTL",
          align: "left",
          field: row => row.ttl,
          sortable: true
        },
        {
          name: "enabled",
          label: "Enabled",
          align: "left",
          field: row => row.enabled,
          sortable: true
        }
      ]
    };
  }
};
</script>

<style></style>
