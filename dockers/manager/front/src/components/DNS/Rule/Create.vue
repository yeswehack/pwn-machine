<template>
  <q-form @submit="submit">
    <q-card-section class="column q-col-gutter-md">
      <q-select
        required
        v-model="form.zone"
        :options="zoneNames"
        label="zone"
        class="col"
      />
      <q-input
        required
        :disable="!form.zone"
        v-model="form.name"
        :rules="[validateName]"
        label="name"
        class="col"
      />
      <div class="row q-gutter-md ">
        <q-toggle :disable="!form.zone" label="Lua record" v-model="form.isLua" />
        <q-select
          :disable="!form.zone"
          v-model="form.type"
          :options="types"
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
      <div class="col editor-container" v-if="isLua">
        <monaco-editor
          v-model="form.records[0].content"
          :options="editorOptions"
          class="editor"
          language="lua"
          theme="vs-dark"
        />
      </div>
      <component
        v-else
        :disable="!form.zone"
        :is="formChildren.records"
        v-model="form.records"
        object-key="content"
        label="Records"
      />
    </q-card-section>
    <q-card-section v-if="0">
      <pre>{{ form }}</pre>
    </q-card-section>
    <q-card-section>
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "../../ListInput.vue";
import api from "src/api";
import MonacoEditor from "vue-monaco";
import ResetAndSave from "src/components/ResetAndSave.vue";

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
  components: { ResetAndSave, MonacoEditor },
  mixins: [DeepForm],
  props: {
    value: Object,
    edit: { type: Boolean }
  },
  apollo: {
    zones: {
      query: api.dns.GET_ZONES,
      update: data => data.dnsZones
    }
  },
  formDefinition: {
    zone: null,
    isLua: false,
    name: null,
    type: null,
    records: ListInput,
    ttl: 3600
  },
  data() {
    const editorOptions = {
      minimap: { enabled: false },
      padding: { bottom: 100, top: 100 },
      lineDecorationsWidth: 5,
      lineNumbers: false,
    };
    return { types, editorOptions };
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
      if (name !== this.form.zone && !name.endsWith(suffix)) {
        return `Name must ends with ${this.form.zone}`;
      }
    },
    submit() {
      const input = {
        ...this.form,
        records: this.form.records.map(r => ({ content: r.content }))
      };

      this.$apollo
        .mutate({
          mutation: api.dns.CREATE_RULE,
          variables: { input },
          refetchQueries: [{ query: api.dns.GET_RULES }]
        })
        .then(() => {
          this.$emit("ok");
        });
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

<style lang="scss" scoped>
.editor-container {
  display: grid;
  grid-template-rows: 300px;
  grid-template-columns: 1fr;
}

.editor {
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 4px;
  overflow: hidden;
  box-sizing: border-box;
}
</style>
