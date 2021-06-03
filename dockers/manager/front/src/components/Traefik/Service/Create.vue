<template>
  <q-form @submit="submit">
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="chooseType">
        <q-input
          v-model="form.name"
          ref="name"
          :rules="[validateName]"
          label="Name"
        />
        <q-select
          v-model="form.protocol"
          label="Protocol"
          :options="Object.keys(availableTypes)"
        />
        <q-select
          :disable="!form.protocol"
          v-model="form.type"
          label="Type"
          :options="availableTypes[form.protocol]"
        />
      </q-tab-panel>
      <q-tab-panel name="enterSettings">
        <component
          ref="create"
          :is="createComponent"
          v-model="form.extra"
          @updateSubtitle="t => $emit('updateSubtitle', t)"
        />
      </q-tab-panel>
    </q-tab-panels>
    <q-card-section>
      <reset-and-save
        :steps="steps"
        :step.sync="panel"
        :modified="modified"
        @reset="reset"
        @save="submit"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm.js";
import CreateHttpLoadBalancer from "./CreateHttpLoadBalancer.vue";
import CreateHttpMirroring from "./CreateHttpMirroring.vue";
import CreateHttpWeighted from "./CreateHttpWeighted.vue";
import CreateTcpLoadBalancer from "./CreateTcpLoadBalancer.vue";
import CreateTcpWeighted from "./CreateTcpWeighted.vue";
import CreateUdpLoadBalancer from "./CreateUdpLoadBalancer.vue";
import CreateUdpWeighted from "./CreateUdpWeighted.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import { notify } from "src/utils";

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

    const steps = [
      {
        name: "chooseType",
        validate: () => {
          return this.$refs.name.validate();
        }
      },
      {
        name: "enterSettings",
        validate: () => {
          return this.$refs.create.validate();
        }
      }
    ];
    return { loading: false, availableTypes, panel: "chooseType", steps };
  },
  watch: {
    currentProtocol(proto, oldProto) {
      const idx = oldProto
        ? this.availableTypes[oldProto].indexOf(this.form.type)
        : 0;
      const availableTypes = this.availableTypes[proto];
      this.form.type =
        availableTypes[idx > availableTypes.length - 1 ? 0 : idx];
      this.changeSubtitle();
    },
    currentType(v, old) {
      if (!old) return;
      const instance = this.instanciateSubForm(
        getCreateComponent(this.form),
        this.form
      );
      this.form.extra = instance.originalForm;
      this.changeSubtitle();
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
    changeSubtitle() {
      this.$emit(
        "updateSubtitle",
        `${this.form.protocol.toUpperCase()} ${this.form.type}`
      );
    },
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
    validateName(val) {
      if (!val) {
        return "You must enter a name.";
      }
    },
    async createService() {
      const protocol = this.form.protocol;
      const type = this.form.type;
      const mutation = api.traefik.services.CREATE_SERVICE[protocol][type];
      const input = {
        name: this.form.name,
        [type]: this.form.extra
      };
      await this.$apollo
        .mutate({
          mutation,
          variables: { input },
          refetchQueries: [{ query: api.traefik.services.LIST_SERVICES }]
        })
        .then(notify(`${this.form.name} created.`))
        .then(r => {
          if (r.success) {
            this.$emit("ok");
          }
        })
    },
    async updateService() {
      const type = this.form.type;
      const mutation = api.traefik.services.UPDATE_SERVICE[type];
      const variables = {
        nodeId: this.service.nodeId,
        patch: this.form.extra
      };
      await this.$apollo
        .mutate({
          mutation,
          variables,
          refetchQueries: [{ query: api.traefik.services.LIST_SERVICES }]
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
    async submit(done) {
      try {
        if (this.edit) {
          await this.updateService();
        } else {
          await this.createService();
        }
      } finally {
        done()
      }
    }
  }
};
</script>
