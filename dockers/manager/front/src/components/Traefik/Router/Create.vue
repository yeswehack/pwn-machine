<template>
  <div>
    <q-card-section>
      <div class="row q-gutter-sm">
        <div class="col">
          <q-input
            ref="name"
            v-model="form.name"
            autofocus
            :rules="[required('You must enter a name.')]"
            label="Name"
          />
        </div>
        <div class="col col-3">
          <q-select
            v-model="form.protocol"
            :options="protocols"
            label="Protocol"
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-pt-none">
      <component ref="create" :is="createComponent" v-model="form.extra" />
    </q-card-section>
    <q-card-section>
      <reset-and-save
        :modified="modified"
        @save="submit"
        :validate="validate"
        @reset="reset"
      />
    </q-card-section>
  </div>
</template>

<script>
import api from "src/api";
import CreateHTTP from "./CreateHTTP.vue";
import CreateTCP from "./CreateTCP.vue";
import CreateUDP from "./CreateUDP.vue";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";

export function getCreateComponent(value) {
  const mapping = {
    http: CreateHTTP,
    tcp: CreateTCP,
    udp: CreateUDP
  };
  return mapping[value?.protocol];
}

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    protocol: null,
    extra: getCreateComponent
  },
  apollo: {
    entrypoints: {
      query: api.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    },
    services: {
      query: api.traefik.services.LIST_SERVICES,
      update: data => data.traefikServices
    }
  },
  data: () => ({ protocols: ["http", "tcp", "udp"] }),
  computed: {
    currentProtocol() {
      return this.form.protocol;
    },
    createComponent() {
      return getCreateComponent(this.form);
    },
    relevantentrypoints() {
      const protocol = this.form.protocol === "udp" ? "udp" : "tcp";
      const entrypoints = (this.entrypoints || []).filter(
        ep => ep.protocol === protocol
      );
      return entrypoints.map(ep => ({
        label: ep.name,
        protocol: ep.protocol
      }));
    },
    relevantServices() {
      const services = (this.services || []).filter(
        s => s.protocol === this.form.protocol
      );
      return services.map(s => ({
        label: s.name,
        protocol: s.protocol
      }));
    }
  },
  watch: {
    currentProtocol(proto, old) {
      if (!old) return;
      const instance = this.instanciateSubForm(
        getCreateComponent(this.form),
        this.form
      );
      this.form.extra = instance.originalForm;
    }
  },
  methods: {
    submit(done) {
      const mutation = api.traefik.routers.CREATE_ROUTER[this.form.protocol];
      const input = {
        name: this.form.name,
        ...this.form.extra
      };
      this.mutate({
        mutation,
        variables: { input },
        refetchQueries: [{ query: api.traefik.routers.LIST_ROUTERS }],
        message: `${this.form.name} created.`
      })
        .then(() => {
          this.$emit("ok");
        })
        .finally(done);
    },
    validate() {
      const validators = [
        this.$refs.name.validate(),
        this.$refs.create.validate()
      ];
      return validators.every(x => x);
    }
  }
};
</script>
