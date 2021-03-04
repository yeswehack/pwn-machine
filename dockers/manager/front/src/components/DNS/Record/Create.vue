<template>
  <q-card bordered style="width: 700px; max-width: 80vw;">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new DNS record</div>
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
            v-model="formData.zone"
            :options="zones"
            label="zone"
          />
        </div>
        <div>
          <q-select
            filled
            v-model="formData.type"
            :options="types"
            label="type"
          />
        </div>
        <div>
          <q-input
            filled
            v-model="formData.record"
            label="record"
            hint="example.com"
          />
        </div>
        <div>
          <q-input
            type="number"
            filled
            min="0"
            v-model="formData.ttl"
            label="TTL"
          />
        </div>
        <div>
          <q-toggle
            filled
            v-model="formData.enable"
            label="Enable"
            color="green"
          />
        </div>
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md q-gutter-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: {},
  data() {
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
    return { zones: ["test"], types };
  },
  methods: {
    submit() {
      this.$emit("submit", this.formData);
    }
  }
};
</script>
