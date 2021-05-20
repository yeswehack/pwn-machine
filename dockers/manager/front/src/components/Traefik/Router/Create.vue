<template>
  <div>
    <q-card-section class="">
      <q-input v-model="form.name" autofocus required label="Name" />
      <q-select
        v-model="form.protocol"
        :options="protocols"
        required
        :rules="[nonEmpty]"
        label="Protocol"
      />
    </q-card-section>
    <component :is="createComponent" v-model="form.extra" />
    <q-card-section>
      <reset-and-save :modified="modified" @save="submit" @reset="reset" />
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
  console.log("value", value);
  return mapping[value?.protocol] ?? null;
}

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    protocol: null,
    extra(value) {
      return getCreateComponent(value);
    }
  },
  apollo: {
    entrypoints: {
      query: api.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    },
    services: {
      query: api.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
  },
  data() {
    const protocols = ["http", "tcp", "udp"];
    return { protocols };
  },
  computed: {
    currentProtocol() {
      return this.form.protocol;
    },
    createComponent() {
      return getCreateComponent(this.form);
    },
    relevantentrypoints() {
      const protocol = this.form.protocol == "udp" ? "udp" : "tcp";
      const entrypoints = (this.entrypoints || []).filter(
        ep => ep.protocol == protocol
      );
      return entrypoints.map(ep => ({
        label: ep.name,
        protocol: ep.protocol
      }));
    },
    relevantServices() {
      const services = (this.services || []).filter(
        s => s.protocol == this.form.protocol
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
    submit() {
      const input = {
        name: this.form.name,
        protocol: this.form.protocol,
        ...this.form.extra
      };
      /* this.$apollo
        .mutate({
          mutation: api.traefik.CREATE_ROUTER,
          variables: { input },
          refetchQueries: [{ query: api.traefik.GET_ROUTERS }]
        })
        .then(r => {
          this.$emit("ok");
        }); */
    },
    nonEmpty(val) {
      if (val === null || val === undefined) {
        return "You must make a selection.";
      }
    }
  }
};
</script>
