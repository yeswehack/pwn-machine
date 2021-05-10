<template>
  <q-card bordered class="create-network">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new bridge network</div>
          <q-space />
          <HelpLink
            href="https://docs.docker.com/engine/reference/commandline/network_create/"
          />
          <q-btn icon="eva-close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <q-input v-model="formData.name" filled required label="Name" />
        <q-checkbox label="Internal" v-model="formData.internal" />
      </q-card-section>
      <q-card-section class="q-gutter-sm">
        <q-expansion-item
          expand-separator
          header-style="background :#2d2d2d !important"
          icon="eva-share-outline"
          label="IPAM Settings"
          :caption="ipamCaption"
        >
          <q-list :padding="true">
            <q-item>
              <q-item-section>
                <q-input
                  filled
                  clearable
                  v-model="formData.subnet"
                  label="Subnet"
                />
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section>
                <q-input
                  filled
                  clearable
                  v-model="formData.gateway"
                  label="gateway"
                />
              </q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
        <q-expansion-item
          header-style="background :#2d2d2d !important"
          expand-separator
          :caption="`${formData.labels.length} label(s)`"
          icon="label"
          label="Labels"
        >
          <div class="q-py-md">
            <KeyValueTable
              v-model="formData.labels"
              hide-bottom
              class="bg-grey-10"
            />
          </div>
        </q-expansion-item>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";
import HelpLink from "src/components/HelpLink.vue";
import DeepForm from "src/mixins/DeepForm.js";
import gql from "src/gql";

export default {
  mixins: [DeepForm],
  components: { KeyValueTable, HelpLink },
  computed: {
    ipamCaption() {
      return this.formData.subnet || this.formData.gateway
        ? "custom"
        : "automatic";
    }
  },
  methods: {
    createDefaultForm() {
      return {
        name: "",
        internal: false,
        subnet: null,
        range: null,
        gateway: null,
        labels: []
      };
    },
    async submit() {
      const f = this.formData;
      const variables = {
        name: f.name,
        internal: f.internal,
        gateway: f.gateway,
        subnet: f.subnet,
        labels: f.labels
      };

      this.runMutation(
        gql.docker.CREATE_NETWORK,
        variables,
        `Network ${f.name} created.`,
        (store, { network }) => {
          const data = store.readQuery({ query: gql.docker.GET_NETWORKS });
          data.docker.networks = data.docker.networks
            .filter(n => n.id != network.id)
            .concat([network]);
          store.writeQuery({ query: gql.docker.GET_NETWORKS, data });
          this.$emit("close");
        }
      );
    }
  }
};
</script>

<style>
.create-network {
  min-width: 700px;
  max-width: 80vw;
}
</style>
