<template>
  <q-card bordered style="width: 700px; max-width: 80vw;">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new DNS zone</div>
          <q-space />
          <HelpLink
            href="https://doc.powerdns.com/authoritative/http-api/zone.html"
          />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <div class="q-pt-md">
        <SoaForm required filled v-model="formData.soa" no-buttons>
          <template #before>
            <q-item>
              <q-item-section>
                <q-item-label>
                  <q-input required filled v-model="formData.name" label="Name" />
                </q-item-label>
              </q-item-section>
            </q-item>
          </template>
          <template #after> </template>
        </SoaForm>
      </div>
      <q-card-actions align="right" class="q-pa-md q-gutter-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import HelpLink from "src/components/HelpLink.vue";
import SoaForm from "src/components/DNS/Zone/SoaForm.vue";
import DeepForm from "src/mixins/DeepForm.js";

//import graphql from "src/gql/dns";
/* const {
  mutations: { createDnsZone },
  queries: { getDnsZones }
} = graphql; */

export default {
  mixins: [DeepForm],
  components: { HelpLink, SoaForm },
  methods: {
    createDefaultForm() {
      return {
        name: "",
        soa: {
          refresh: 86400,
          retry: 7200,
          expire: 3600000,
          ttl: 172800
        }
      };
    },
    submit() {
      const f = this.formData;
      const variables = {
        name: f.name,
        soa: {
          nameserver: f.soa.nameserver,
          postmaster: f.soa.postmaster,
          refresh: f.soa.refresh,
          retry: f.soa.retry,
          expire: f.soa.expire,
          ttl: f.soa.ttl
        }
      };
      this.runMutation(
        createDnsZone,
        variables,
        `Zone ${f.name} created.`,
        (store, { zone }) => {
          const data = store.readQuery({ query: getDnsZones });
          data.dns.zones = data.dns.zones
            .filter(z => z.id != zone.id)
            .concat([zone]);
          store.writeQuery({ query: getDnsZones, data });
          this.$emit("close");
        }
      );
    }
  }
};
</script>
