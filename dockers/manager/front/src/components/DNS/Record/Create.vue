<template>
  <q-card bordered style="width: 700px; max-width: 80vw;">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new DNS rule</div>
          <q-space />
          <a
            class="text-white"
            href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            target="_blank"
          >
            <q-icon size="sm" name="help" />
          </a>
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <div>
          <q-select
            filled
            required
            v-model="ruleForm.zone"
            :options="zones"
            label="zone"
          />
        </div>
        <div>
          <q-input
            filled
            required
            :disable="!ruleForm.zone"
            :suffix="`.${ruleForm.zone}`"
            v-model="ruleForm.name"
            label="name"
          />
        </div>
        <div>
          <q-select
            filled
            :disable="!ruleForm.zone"
            v-model="ruleForm.type"
            :options="types"
            label="type"
          />
        </div>
        <div>
          <q-input
            :disable="!ruleForm.zone"
            type="number"
            filled
            min="0"
            v-model="ruleForm.ttl"
            label="TTL"
          />
        </div>
        <div>
          <EditTable
            :disable="!ruleForm.zone"
            title="Records"
            :columns="recordColumns"
            :createDefault="createPair"
            v-model="ruleForm.records"
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
        {{ ruleForm }}
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import gql from "graphql-tag";
import EditTable from "src/components/EditTable.vue";

const ruleFragment = gql`
  fragment ruleFragment on Rule {
    id
    zone
    type
    name
    records {
      content
      enabled
    }
    ttl
  }
`;

const createOrModifyDnsRule = gql`
  mutation createOrModifyDnsRule(
    $zone: String!
    $name: String!
    $type: String!
    $ttl: Int!
    $records: [RecordInput!]
  ) {
    createOrModifyDnsRule(
      rule: {
        zone: $zone
        name: $name
        type: $type
        ttl: $ttl
        records: $records
      }
    ) {
      rule {
        ...ruleFragment
      }
    }
  }
  ${ruleFragment}
`;

export default {
  components: { EditTable },
  apollo: {
    zones: {
      query: gql`
        query getZoneNames {
          dns {
            zones {
              id
              name
            }
          }
        }
      `,
      update: ({ dns: { zones } }) => zones.map(z => z.name)
    }
  },
  data() {
    const ruleForm = {
      zone: "",
      type: "A",
      records: [],
      enable: true,
      ttl: 3600
    };
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
    return { types, ruleForm, recordColumns };
  },
  methods: {
    createPair() {
      return { content: "", enabled: true };
    },
    submit() {
      this.$apollo.mutate({
        mutation: createOrModifyDnsRule,
        variables: this.ruleForm
      });
    }
  }
};
</script>
