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
import gql from "graphql-tag";

export default {
  components: { BaseTable, CreateZone },
  apollo: {
    zones: {
      query: gql`
        {
          dns {
            zones {
              id
              name
              serial
              info {
                id
                soa {
                  nameserver
                  postmaster
                  refresh
                  retry
                  expire
                  ttl
                }
              }
            }
          }
        }
      `,
      update: data => data.dns.zones
    }
  },
  methods: {
    async createZone(z) {
      const r = await this.$api.dns.createZone(z);
      console.log(r);
      this.$refs.table.closePopup();
    },
    cloneZone(zone) {
      this.zoneForm = zone;
    }
  },
  computed: {
    loading(){
      return this.$apollo.queries.zones.loading
    }
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

    return {
      zoneForm,
      columns: [
        {
          name: "name",
          align: "left",
          label: "Name",
          field: "name"
        },
        {
          name: "nameserver",
          align: "left",
          label: "Nameserver",
          field: r => r.info.soa.nameserver
        },
        {
          name: "postmaster",
          align: "left",
          label: "Postmaster",
          field: r => r.info.soa.postmaster
        },
        {
          name: "serial",
          align: "left",
          label: "Serial",
          field: "serial"
        },
        {
          name: "refresh",
          align: "left",
          label: "Refresh",
          field: r => r.info.soa.refresh
        },
        {
          name: "retry",
          align: "left",
          label: "retry",
          field: r => r.info.soa.retry
        },
        {
          name: "expire",
          align: "left",
          label: "Expire",
          field: r => r.info.soa.expire
        },
        {
          name: "ttl",
          align: "left",
          label: "TTL",
          field: r => r.info.soa.ttl
        },
      ]
    };
  }
};
</script>

<style></style>
