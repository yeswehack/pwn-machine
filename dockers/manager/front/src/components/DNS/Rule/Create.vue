<template>
  <q-form @submit="submit">
    <q-card-section class="q-col-gutter-md">
      <q-select
        filled
        required
        v-model="form.zone"
        :options="zoneNames"
        label="zone"
      />
      <q-input
        filled
        required
        :disable="!form.zone"
        v-model="form.name"
        :rules="[validateName]"
        label="name"
      />
      <q-select
        filled
        :disable="!form.zone"
        v-model="form.type"
        :options="types"
        label="type"
      />
      <q-input
        :disable="!form.zone"
        type="number"
        filled
        min="0"
        v-model.number="form.ttl"
        label="TTL"
      />
      <component
        :disable="!form.zone"
        :is="formChildren.records"
        v-model="form.records"
        object-key="content"
        label="Records"
      />
    </q-card-section>
    <q-card-section>
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "../../ListInput.vue";
import db from "src/gql";
import ResetAndSave from "src/components/ResetAndSave.vue";

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
  components: { ResetAndSave },
  mixins: [DeepForm],
  props: {
    value: Object,
    edit: { type: Boolean }
  },
  apollo: {
    zones: {
      query: db.dns.GET_ZONES,
      update: data => data.dnsZones
    }
  },
  formDefinition: {
    zone: null,
    name: null,
    type: null,
    records: ListInput,
    ttl: 3600
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
  computed: {
    zoneNames() {
      return (this.zones ?? []).map(z => z.name);
    }
  },
  methods: {
    validateName(name) {
      const suffix = "." + this.form.zone;
      if (name !== this.form.zone && !name.endsWith(suffix)) {
        return `Name must ends with ${this.form.zone}`;
      }
    },
    createRecord() {
      return { content: "", enabled: true };
    },
    submit() {
      const input = {
        ...this.form,
        records: this.form.records.map(r => ({ content: r.content }))
      };

      this.$apollo
        .mutate({
          mutation: db.dns.CREATE_RULE,
          variables: { input },
          refetchQueries: [{ query: db.dns.GET_RULES }]
        })
        .then(() => {
          this.$emit("ok");
        });
    }
  }
};
</script>
