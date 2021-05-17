<template>
  <div class="row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">{{ network.name }}</div>
            <q-space />
            <help-link
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <ipam-input readonly :value="network.ipam" />
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <label-input readonly :value="network.labels" />
        </q-card-section>
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section>
          <container-list-input
            v-model="network.containers"
            title="Connected containers"
          />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import gql from "src/api";
import IpamInput from "./IpamInput.vue";
import LabelInput from "../LabelInput.vue";
import DeepForm from "src/mixins/DeepForm";
import HelpLink from "src/components/HelpLink.vue";
import ContainerListInput from "../ContainerListInput.vue";

export default {
  props: {
    network: { type: Object, required: true }
  },
  components: {
    IpamInput,
    LabelInput,
    HelpLink,
    ContainerListInput
  },
  methods: {
    refresh() {
      this.$apollo.queries.network.refetch();
    }
  },
  computed: {
    IPAMConfig() {
      return [
        { key: "Gateway", value: this.network.gateway },
        { key: "Subnet", value: this.network.subnet }
      ];
    }
  }
};
</script>
