<template>
  <div style="width: 600px; max-width: 80vw;">
    <q-card bordered>
      <q-form @submit="submit">
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">Create a new DNS rule</div>
            <q-space />
            <HelpLink
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
            <q-btn
              icon="eva-close"
              flat
              round
              dense
              v-close-popup
              v-if="!edit"
            />
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-col-gutter-md">
          <div>
            <q-select
              filled
              required
              v-model="formData.zone"
              :options="zones"
              label="zone"
            />
          </div>
          <div>
            <q-input
              filled
              required
              :disable="!formData.zone"
              :suffix="`.${formData.zone}`"
              v-model="formData.name"
              label="name"
            />
          </div>
          <div>
            <q-select
              filled
              :disable="!formData.zone"
              v-model="formData.type"
              :options="types"
              label="type"
            />
          </div>
          <div>
            <q-input
              :disable="!formData.zone"
              type="number"
              filled
              min="0"
              v-model="formData.ttl"
              label="TTL"
            />
          </div>
          <div>
            <EditTable
              class="bg-grey-10"
              hide-bottom
              :disable="!formData.zone"
              title="Records"
              :columns="recordColumns"
              :createDefault="createRecord"
              v-model="formData.records"
            >
              <template v-slot:body-cell-enabled="props">
                <q-td>
                  <div class="row">
                    <q-space />
                    <q-toggle slot="" v-model="props.row['enabled']" />
                  </div>
                </q-td>
              </template>
            </EditTable>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="q-pa-md q-gutter-md">
          <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
            Create
          </q-btn>
        </q-card-actions>
      </q-form>
    </q-card>
  </div>
</template>

<script>
import EditTable from "src/components/EditTable.vue";
import HelpLink from "src/components/HelpLink.vue";
import DeepForm from "src/mixins/DeepForm.js";

import graphql from "src/gql/dns";
const {
  mutations: { createDnsRule },
  queries: { getRules, getZoneNames }
} = graphql;

const types = [
  "A",
  "AAAA",
  "AFSDB",
  "ALIAS",
  "APL",
  "CAA",
  "CERT",
  "CDNSKEY",
  "CDS",
  "CNAME",
  "DNSKEY",
  "KEY",
  "LOC",
  "MX",
  "NAPTR",
  "NS",
  "NSEC",
  "NSEC3",
  "NSEC3PARAM",
  "OPENPGPKEY",
  "PTR",
  "RP",
  "RRSIG",
  "SOA",
  "SPF",
  "SSHFP",
  "SRV",
  "TKEY",
  "TSIG",
  "TLSA",
  "SMIMEA",
  "TXT",
  "URI"
];

export default {
  mixins: [DeepForm],
  components: { EditTable, HelpLink },
  props: {
    value: Object,
    edit: { type: Boolean }
  },
  apollo: {
    zones: {
      query: getZoneNames,
      update: ({ dns: { zones } }) => zones.map(z => z.name)
    }
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

    return { types, recordColumns };
  },
  methods: {
    createDefaultForm() {
      return {
        zone: "",
        name: "",
        type: "",
        records: [],
        ttl: 3600
      };
    },
    createRecord() {
      return { content: "", enabled: true };
    },
    submit() {
      const f = this.formData;
      const variables = {
        zone: f.zone,
        name: f.name,
        type: f.type,
        records: f.records.map(({content, enabled}) => ({content, enabled})),
        ttl: f.ttl
      }
      this.runMutation(
        createDnsRule,
        variables,
        `Dns rule ${this.formData.type} ${this.formData.name} created`,
        (store, { rule }) => {
          const data = store.readQuery({ query: getRules });
          data.dns.rules = data.dns.rules
            .filter(r => r.id != rule.id)
            .concat([rule]);
          store.writeQuery({ query: getRules, data });
          this.$emit("close");
        }
      );
    }
  }
};
</script>
