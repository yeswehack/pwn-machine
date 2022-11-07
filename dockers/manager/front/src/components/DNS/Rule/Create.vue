<template>
  <q-form @submit="submit">
    <q-card-section class="column q-col-gutter-md">
      <q-select
        ref="zone"
        v-model="form.zone"
        :rules="[required('Please choose a zone')]"
        :options="zoneNames"
        label="zone"
        class="col"
      />
      <q-input
        ref="name"
        v-model="form.name"
        :disable="!form.zone"
        :rules="[validateName]"
        label="name"
        class="col"
      />
      <div class="row q-gutter-md ">
        <q-toggle
          v-model="form.isLua"
          :disable="!form.zone"
          label="Lua record"
        />
        <q-select
          ref="type"
          v-model="form.type"
          :disable="!form.zone"
          :rules="[required('Please choose a type')]"
          :options="types"
          class="col"
          label="type"
        />
        <q-input
          v-model.number="form.ttl"
          :disable="!form.zone"
          type="number"
          min="0"
          class="col"
          label="TTL"
        />
      </div>
      <lua-editor v-if="isLua" ref="records" v-model="form.records[0].content" />
      <component
        :is="formChildren.records"
        v-else
        ref="records"
        v-model="form.records"
        :disable="!form.zone"
        label="Records"
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
    edit: { type: Boolean, default: false }
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
  data: () => ({ types }),
  computed: {
    zoneNames() {
      return (this.zones ?? []).map(z => z.name);
    },
    isLua() {
      return this.form.isLua;
    }
  },
  watch: {
    isLua(v) {
      if (v && this.form.records.length === 0) {
        this.form.records = [{ content: "return ''" }];
      }
    }
  },
  methods: {
    validateName(name) {
      return (
        name === this.form.zone ||
        name?.endsWith("." + this.form.zone) ||
        `Name must ends with ${this.form.zone}`
      );
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
      console.log(this.form)
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
  }
};
</script>
