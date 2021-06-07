<template>
  <div>
    <q-card-section>
      <div class="row q-gutter-sm">
        <div class="col">
          <q-input
            ref="name"
            label="Name"
            autofocus
            :rules="[required('You must enter a name.')]"
            v-model="form.name"
          />
        </div>
        <div class="col col-3">
          <q-select
            label="Protocol"
            :options="protocols"
            v-model="form.protocol"
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
    protocol: "http",
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
    validate() {
      const validators = [
        this.$refs.name.validate(),
        this.$refs.create.validate()
      ];
      return validators.every(x => x);
    },
    submit(done) {
      this.mutate({
        mutation: api.traefik.routers.CREATE_ROUTER[this.form.protocol],
        variables: { input: { name: this.form.name, ...this.form.extra } },
        refetchQueries: [{ query: api.traefik.routers.LIST_ROUTERS }],
        message: `${this.form.name} created.`
      })
        .then(() => {
          this.$emit("ok");
        })
        .finally(done);
    }
  }
};
</script>
