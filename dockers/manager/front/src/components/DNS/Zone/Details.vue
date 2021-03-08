<template>
  <div class=" row q-col-gutter-md q-py-md">
    <div class="col-6">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">Zone: {{ zone.name }}</div>
            <q-space />
            <div title="Serial" class="text-mono">{{ zone.serial }}</div>
            <HelpLink
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <SoaForm  :value="zone.soa" @submit="updateSOA" />
        </q-card-section>
      </q-card>
    </div>
    <div class="col-6">
      <div class="col col-12">
        <LogList :domain="`*${zone.name}`" type="*" />
      </div>
    </div>
  </div>
</template>
<script>
import HelpLink from "src/components/HelpLink.vue";
import SoaForm from "./SoaForm.vue";
import LogList from "src/components/DNS/LogList.vue";
import graphql from "src/gql/dns";
const {
  mutations: { modifySoaForDnsZone }
} = graphql;

export default {
  components: { HelpLink, SoaForm, LogList },
  props: {
    zone: Object
  },
  data() {
    const recordColumns = [
      {
        name: "content",
        align: "left",
        label: "content",
        field: "content",
        headerStyle: "width: 90%"
      },
      {
        name: "enabled",
        align: "left",
        label: "enabled",
        field: "enabled",
        headerStyle: "width: 10%"
      }
    ];
    return { ttl: 0, recordColumns, records: [] };
  },
  methods: {
    updateSOA(f) {
      const variables = {
        soa: {
          nameserver: f.nameserver,
          postmaster: f.postmaster,
          refresh: f.refresh,
          retry: f.retry,
          expire: f.expire,
          ttl: f.ttl
        },
        zone: this.zone.name
      };
      this.runMutation(
        modifySoaForDnsZone,
        variables,
        `SOA rule modified for ${this.zone.name}`
      );
    }
  }
};
</script>

<style></style>
