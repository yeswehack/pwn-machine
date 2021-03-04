<template>
  <BaseTable
    ref="table"
    name="zone"
    rkey="id"
    :expendable="true"
    :loading="loading"
    :data="zones"
    :columns="columns"
    v-on:cloneRow="cloneZone"
  >
    <template #popup>
      <CreateZone v-model="zoneForm" v-on:submit="createZone" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import CreateZone from "src/components/DNS/Zone/Create.vue";
import { mapGetters } from "vuex";
import { date } from "quasar";

export default {
  components: { BaseTable, CreateZone },
  props: {
    zones: Array,
    records: Array
  },
  methods: {
    async createZone(z) {
      const r = await this.$api.dns.createZone(z)
      console.log(r)
      this.$refs.table.closePopup();
    },
    getRecordCount(id) {
      const record = this.records.find(r => r.id == id);
      return record ? record.rrsets.length : 0;
    },
    getSOA(id) {
      const record = this.records.find(r => r.id == id);
      if (!record) return null;
      const rrset = record.rrsets.find(r => r.type == "SOA");
      if (!rrset) return null;
      const soa = rrset.records[0].content;
      return soa;
    },
    getSOAItem(soa, item) {
      return soaRegex.exec(soa).groups[item];
    },
    cloneZone(zone) {
      this.zoneForm = zone;
    },
  },
  computed: {
    ...mapGetters(["loading"]),
  },
  data() {
    const defaultSerial = date.formatDate(Date.now(), "YYYYMMDD01");
    const zoneForm = {
      name: "",
      postmaster: "",
      serial: defaultSerial,
      refresh: 86400,
      retry: 7200,
      expire: 3600000,
      ttl: 172800
    };

    const capitalize = s => s.charAt(0).toUpperCase() + s.slice(1);
    const field = (name, opt = {}) => ({
      name,
      align: "left",
      label: capitalize(name),
      field: name,
      sortable: true,
      ...opt
    });
    return {
      zoneForm,
      columns: [
        field("name"),
        field("nameserver"),
        field("postmaster"),
        field("serial"),
        field("refresh"),
        field("retry"),
        field("expire"),
        field("ttl", {label: "TTL"}),
      ]
    };
  }
};
</script>

<style></style>
