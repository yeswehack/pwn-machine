<template>
  <q-expansion-item
    label="Network"
    :caption="selectedName"
    icon="eva-globe-outline"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <q-select
          v-model="network"
          label="Network name"
          :options="dockerNetworks"
          option-label="name"
          clearable
        />
      </q-card-section>
      <q-card-section>
        <div class="row justify-end">
          <q-btn
            dense
            color="positive"
            icon="eva-plus"
            label="Create a new network"
            @click="createNetwork"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import api from "src/api";
import NetworkDialog from "../../Network/Dialog.vue";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    dockerNetworks: {
      query: api.docker.networks.LIST_NETWORKS
    }
  },
  data: () => ({ network: null }),
  computed: {
    selectedName() {
      return this.network?.name;
    }
  },
  watch: {
    network(selected) {
      this.form = selected?.id;
    }
  },
  methods: {
    createNetwork() {
      this.$q.dialog({
        component: NetworkDialog,
        parent: this
      });
    }
  }
};
</script>
