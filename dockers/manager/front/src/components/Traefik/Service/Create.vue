<template>
  <q-form @submit="submit">
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="chooseType">
        <q-input v-model="form.name" required label="Name" :rule="[nonEmpty]" />
        <q-select
          v-model="form.protocol"
          required
          label="Protocol"
          :options="Object.keys(availableTypes)"
        />
        <q-select
          :disable="!form.protocol"
          v-model="form.type"
          required
          label="Type"
          :options="availableTypes[form.protocol]"
        />
        <q-card-actions class="q-mt-md" align="right">
          <q-btn color="warning" label="Cancel" @click="$emit('cancel')" />
          <q-btn
            color="positive"
            label="Next"
            @click="panel = 'enterSettings'"
          />
        </q-card-actions>
      </q-tab-panel>
      <q-tab-panel name="enterSettings">
        <create-http-load-balancer
          v-model="form.extra"
          v-if="form.protocol == 'http' && form.type == 'loadBalancer'"
        />
        <create-http-mirroring
          v-model="form.extra"
          v-if="form.protocol == 'http' && form.type == 'mirroring'"
        />
        <create-http-weighted
          v-model="form.extra"
          v-if="form.protocol == 'http' && form.type == 'weighted'"
        />

        <create-tcp-load-balancer
          v-model="form.extra"
          v-if="form.protocol == 'tcp' && form.type == 'loadBalancer'"
        />
        <create-tcp-weighted
          v-model="form.extra"
          v-if="form.protocol == 'tcp' && form.type == 'weighted'"
        />

        <create-udp-load-balancer
          v-model="form.extra"
          v-if="form.protocol == 'udp' && form.type == 'loadBalancer'"
        />
        <create-udp-weighted
          v-model="form.extra"
          v-if="form.protocol == 'udp' && form.type == 'weighted'"
        />

        <q-card-actions class="q-mt-md" align="right">
          <q-btn
            color="warning"
            :label="cancelBtnLabel"
            @click="cancelBtnClick"
          />
          <q-btn
            color="positive"
            :loading="loading"
            label="Create"
            @click="createService"
          />
        </q-card-actions>
      </q-tab-panel>
    </q-tab-panels>
    <q-card-section>
      {{ form }}
    </q-card-section>
  </q-form>
</template>

<script>
import db from "src/gql";
import DeepForm from "src/mixins/DeepForm.js";
import CreateHttpLoadBalancer from "./CreateHttpLoadBalancer.vue";
import CreateHttpMirroring from "./CreateHttpMirroring.vue";
import CreateHttpWeighted from "./CreateHttpWeighted.vue";
import CreateTcpLoadBalancer from "./CreateTcpLoadBalancer.vue";
import CreateTcpWeighted from "./CreateTcpWeighted.vue";
import CreateUdpLoadBalancer from "./CreateUdpLoadBalancer.vue";
import CreateUdpWeighted from "./CreateUdpWeighted.vue";
export default {
  components: {
    CreateHttpLoadBalancer,
    CreateHttpMirroring,
    CreateHttpWeighted,
    CreateTcpLoadBalancer,
    CreateTcpWeighted,
    CreateUdpLoadBalancer,
    CreateUdpWeighted
  },
  mixins: [DeepForm],
  props: {
    edit: { type: Boolean, default: false },
    service: { type: Object, default: null }
  },
  data() {
    const availableTypes = {
      http: ["loadBalancer", "mirroring", "weighted"],
      tcp: ["loadBalancer", "weighted"],
      udp: ["loadBalancer", "weighted"]
    };
    const cache = {
      http: {},
      tcp: {},
      udp: {}
    };
    return { loading: false, availableTypes, cache, panel: "chooseType" };
  },
  computed: {
    okBtnLabel() {
      return this.panel == "chooseType" ? "Next" : "Create";
    },
    cancelBtnLabel() {
      return this.panel == "chooseType" ? "Cancel" : "Back";
    }
  },
  methods: {
    okBtnClick() {
      if (this.panel == "chooseType") {
        this.panel = "enterSettings";
      }
    },
    cancelBtnClick() {
      if (this.panel == "enterSettings") {
        this.panel = "chooseType";
      } else {
        this.$emit("cancel");
      }
    },
    createDefaultForm(service) {
      const form = {
        protocol: "http",
        type: "loadBalancer",
        extra: {}
      };
      if (service) {
        form.name = service.name.split("@")[0];
        form.protocol = service.protocol;
        form.type = service.type;
        extra = service[service.type];
      }

      console.log("CREATE DEFAULT FORM", service, form);
      return form;
    },
    nonEmpty(val) {
      if (val === null || val === undefined) {
        return "You must make a selection.";
      }
    },
    nonEmptyArray(val) {
      if (val === null || val === undefined || val.length == 0) {
        return "You must make a selection.";
      }
    },
    async createService() {
      this.loading = true;
      const protocol = this.form.protocol;
      const type = this.form.type;
      const mutation = db.traefik.CREATE_SERVICE[protocol][type];
      const input = {
        name: this.form.name,
        [type]: { ...this.form.extra, __typename: undefined }
      };
      await this.$apollo
        .mutate({
          mutation,
          variables: { input },
          refetchQueries: [{ query: db.traefik.GET_SERVICES }]
        })
        .then(r => {
          this.$emit("ok");
        });
    },
    async updateService() {
      const type = this.form.type;
      const mutation = db.traefik.UPDATE_SERVICE[type];
      const variables = {
        nodeId: this.service.nodeId,
        patch: { ...this.form.extra, __typename: undefined }
      };
      await this.$apollo
        .mutate({
          mutation,
          variables,
          refetchQueries: [{ query: db.traefik.GET_SERVICES }]
        })
        .then(r => {
          this.$emit("ok");
        })
        .catch(r => {
          this.$q.notify({
            message: `Unable to update ${this.service.name}.`,
            type: "negative"
          });
        });
    },
    async submit() {
      this.loading = true;
      try {
        if (this.edit) {
          await this.updateService();
        } else {
          await this.createService();
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
