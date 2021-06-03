<template>
  <q-form @submit="submit">
    <q-card-section class="column q-col-gutter-md">
      <q-select
        :rules="[required('Please choose a zone')]"
        v-model="form.zone"
        :options="zoneNames"
        ref="zone"
        label="zone"
        class="col"
      />
      <q-input
        :disable="!form.zone"
        ref="name"
        v-model="form.name"
        :rules="[validateName]"
        label="name"
        class="col"
      />
      <div class="row q-gutter-md ">
        <q-toggle
          :disable="!form.zone"
          label="Lua record"
          v-model="form.isLua"
        />
        <q-select
          :disable="!form.zone"
          :rules="[required('Please choose a type')]"
          v-model="form.type"
          :options="types"
          ref="type"
          class="col"
          label="type"
        />
        <q-input
          :disable="!form.zone"
          type="number"
          min="0"
          v-model.number="form.ttl"
          class="col"
          label="TTL"
        />
      </div>
      <lua-editor v-model="form.records[0].content" v-if="isLua" />
      <component
        v-else
        :disable="!form.zone"
        :is="formChildren.records"
        v-model="form.records"
        object-key="content"
        label="Records"
        ref="records"
      />
    </q-card-section>
    <q-card-section>
      <reset-and-save
        :modified="modified"
        :validate="validate"
        @reset="reset"
        @save="submit"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import api from "src/api";
import ResetAndSave from "src/components/ResetAndSave.vue";
import LuaEditor from "./LuaEditor.vue";
import RuleInput from "./RuleInput.vue";
import { required, requiredArray } from "src/utils/validators";

const types = [
  "A",
  "AAAA",
  "AFSDB",
  "ALIAS",
  "APL",
  "CAA",
  "CDNSKEY",
  "CDS",
  "CERT",
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
  "SMIMEA",
  "SOA",
  "SPF",
  "SRV",
  "SSHFP",
  "TKEY",
  "TLSA",
  "TSIG",
  "TXT",
  "URI"
];

export default {
  components: { ResetAndSave, LuaEditor },
  mixins: [DeepForm],
  props: {
    value: Object,
    edit: { type: Boolean }
  },
  apollo: {
    zones: {
      query: api.dns.zones.LIST_ZONES,
      update: data => data.dnsZones
    }
  },
  formDefinition: {
    zone: null,
    isLua: false,
    name: null,
    type: null,
    records: RuleInput,
    ttl: 3600
  },
  data() {
    return { types, required };
  },
  computed: {
    zoneNames() {
      return (this.zones ?? []).map(z => z.name);
    },
    isLua() {
      return this.form.isLua;
    }
  },
  methods: {
    validateName(name) {
      const suffix = "." + this.form.zone;
      if (!name || (name !== this.form.zone && !name.endsWith(suffix))) {
        return `Name must ends with ${this.form.zone}`;
      }
    },
    validate() {
      const validators = [
        this.$refs.zone.validate(),
        this.$refs.name.validate(),
        this.$refs.type.validate(),
        this.$refs.records.validate()
      ];
      return validators.every(x => x);
    },
    submit(done) {
      const input = {
        ...this.form,
        records: this.form.records.map(r => ({ content: r.content }))
      };

      this.mutate({
        mutation: api.dns.rules.CREATE_RULE,
        variables: { input },
        refetchQueries: [{ query: api.dns.rules.LIST_RULES }],
        message: `${this.form.name} created`
      })
        .then(() => this.$emit("ok"))
        .finally(done);
    }
  },
  watch: {
    isLua(v) {
      if (v && this.form.records.length == 0) {
        this.form.records = [{ content: "return ''" }];
      }
    }
  }
};
</script>
