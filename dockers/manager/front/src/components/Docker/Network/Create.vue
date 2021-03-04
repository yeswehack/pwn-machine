<template>
  <q-card bordered class="create-network">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new bridge network</div>
          <q-space />
          <a
            class="text-white"
            href="https://docs.docker.com/engine/reference/commandline/network_create/"
            target="_blank"
          >
            <q-icon size="sm" name="help" />
          </a>
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <q-input v-model="form.name" filled required label="Name" />
        <q-checkbox label="Internal" v-model="form.internal" />
        <div>
          <q-expansion-item
            expand-separator
            icon="settings"
            label="IPAM Settings"
            :caption="ipamCaption"
          >
            <div class="q-py-md q-gutter-sm">
              <q-input
                filled
                dense
                clearable
                hint="172.28.0.0/16"
                v-model="form.subnet"
                label="Subnet"
              />
              <q-input
                filled
                dense
                clearable
                hint="172.28.5.0/24"
                v-model="form.range"
                label="IP range"
              />
              <q-input
                filled
                dense
                clearable
                hint="172.28.5.254"
                v-model="form.gateway"
                label="gateway"
              />
            </div>
          </q-expansion-item>
          <q-expansion-item
            expand-separator
            :caption="`${Object.keys(form.labels).length} label(s)`"
            icon="label"
            label="Labels"
          >
            <div class="q-py-md">
              <KeyValueTable v-model="form.labels" />
            </div>
          </q-expansion-item>
        </div>
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

export default {
  components: { KeyValueTable },
  props: {
    info: {
      type: Object,
      default: null
    }
  },
  data() {
    const form = {
      name: "",
      internal: false,
      subnet: null,
      range: null,
      gateway: null,
      labels: {}
    };
    if (this.info) {
      form.name = this.info.Name;
      Object.assign(form.labels, this.info.Labels);
    }
    return { form };
  },
  computed: {
    ipamCaption() {
      return this.form.subnet || this.form.range || this.form.gateway
        ? "custom"
        : "automatic";
    }
  },
  methods: {
    async submit() {
      const network = {
        Name: this.form.name,
        Internal: this.form.internal,
        Labels: this.form.labels,
        IPAM: null
      };
      if (this.editIPAM) {
        network.IPAM = {};
        if (this.form.subnet) {
          network.IPAM.Subnet = this.form.subnet;
        }
        if (this.form.range) {
          network.IPAM.IPRange = this.form.range;
        }
        if (this.form.gateway) {
          network.IPAM.Gateway = this.form.gateway;
        }
      }
      const response = await this.$api.docker.createNetwork(network);

      if ("error" in response) {
        this.$q.notify({
          color: "negative",
          message: response.error
        });
      } else {
        this.$q.notify({
          color: "positive",
          message: `Network ${this.form.name} created.`
        });
        this.$emit("created", response.name);
      }
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
