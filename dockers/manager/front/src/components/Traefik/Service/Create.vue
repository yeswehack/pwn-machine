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
      </q-tab-panel>
      <q-tab-panel name="enterSettings">
        <component :is="createComponent" v-model="form.extra" />
      </q-tab-panel>
    </q-tab-panels>
    <q-card-section>
      <reset-and-save
        :steps="['chooseType', 'enterSettings']"
        :step.sync="panel"
        :modified="modified"
        @reset="reset"
        @save="submit"
      />
    </q-card-section>
    <q-card-section v-if="0">
      <pre>
      {{ form }}
      </pre>
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
import ResetAndSave from "src/components/ResetAndSave.vue";

export function getCreateComponent(value) {
  const mapping = {
    http: {
      loadBalancer: CreateHttpLoadBalancer,
      weighted: CreateHttpWeighted,
      mirroring: CreateHttpMirroring
    },
    tcp: {
      loadBalancer: CreateTcpLoadBalancer,
      weighted: CreateTcpWeighted
    },
    udp: {
      loadBalancer: CreateUdpLoadBalancer,
      weighted: CreateUdpWeighted
    }
  };
  return mapping[value?.protocol]?.[value?.type] ?? CreateHttpLoadBalancer;
}

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  props: {
    edit: { type: Boolean, default: false },
    service: { type: Object, default: null }
  },
  formDefinition: {
    name: null,
    protocol: "http",
    type: "loadBalancer",
    extra(value) {
      return getCreateComponent(value);
    }
  },
  data() {
    const availableTypes = {
      http: ["loadBalancer", "weighted", "mirroring"],
      tcp: ["loadBalancer", "weighted"],
      udp: ["loadBalancer", "weighted"]
    };
    return { loading: false, availableTypes, panel: "chooseType" };
  },
  watch: {
    currentProtocol(proto, oldProto) {
      const idx = oldProto
        ? this.availableTypes[oldProto].indexOf(this.form.type)
        : 0;
      const availableTypes = this.availableTypes[proto];
      this.form.type =
        availableTypes[idx > availableTypes.length - 1 ? 0 : idx];
    },
    currentType() {
      const instance = this.instanciateSubForm(
        getCreateComponent(this.form),
        this.form
      );
      this.form.extra = instance.originalForm;
    }
  },
  computed: {
    currentProtocol() {
      return this.form.protocol;
    },
    currentType() {
      return this.form.type;
    },
    createComponent() {
      return getCreateComponent(this.form);
    },
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
