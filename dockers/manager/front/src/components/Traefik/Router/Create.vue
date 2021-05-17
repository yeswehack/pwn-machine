<template>
  <q-form @submit="createRouter">
    <q-card-section class="q-gutter-sm">
      <q-input v-model="form.name" autofocus required label="Name" v-if="!hideName"/>
      <q-select
        v-model="form.protocol"
        :options="protocols"
        required
        :rules="[nonEmpty]"
        label="Protocol"
        @input="protocolUpdated"
      />
      <q-input
        v-if="form.protocol != 'udp'"
        v-model="form.rule"
        :disable="!form.protocol"
        debounce="100"
        :rules="[validateRule]"
        :hint="
          form.protocol == 'http'
            ? 'ex: Host(`example.com`)'
            : 'ex: HostSNI(`*`)'
        "
        label="Rule"
      />
      <q-select
        v-model="form.entrypoints"
        :disable="!form.protocol"
        multiple
        use-chips
        :rules="[nonEmptyArray]"
        :options="relevantentrypoints"
        label="entrypoints"
      />

      <q-select
        :disable="!form.protocol"
        v-model="form.service"
        :options="relevantServices"
        :rules="[nonEmpty]"
        label="Service"
      >
        <template #after>
          <q-btn
            title="Create a new service"
            round
            dense
            class="bg-green"
            color="positive"
            icon="add"
            @click="createService"
          />
        </template>
      </q-select>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn color="warning" label="Cancel" @click="$emit('cancel')" />
      <q-btn color="positive" type="submit"  label="Create" />
    </q-card-actions>
  </q-form>
</template>

<script>
import ServiceDialog from "../Service/Dialog.vue";
import { extend } from "quasar";
import api from "src/api";
export default {
  props: {
    hideName: {type: Boolean, default: false},
    router: { type: Object, default: null }
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
    const originalForm = {
      name: this.router?.name,
      protocol: this.router?.protocol || "http",
      rule: this.router?.rule,
      entrypoints: this.router?.entryPoints || [],
      service: this.router?.service?.name
    };
    const form = extend(true, {}, originalForm);
    const protocols = ["http", "tcp", "udp"];
    return { form, protocols, originalForm };
  },
  computed: {
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
  methods: {
    reset() {
      this.form = extend(true, {}, originalForm);
    },
    createRouter() {
      const input = {
        name: this.form.name,
        protocol: this.form.protocol,
        rule: this.form.rule,
        entryPoints: this.form.entrypoints.map(e => e.label),
        service: this.form.service.label
      };
      this.$apollo
        .mutate({
          mutation: api.traefik.CREATE_ROUTER,
          variables: { input },
          refetchQueries: [{ query: api.traefik.GET_ROUTERS }]
        })
        .then(r => {
          this.$emit("ok");
        });
    },
    createService() {
      this.$q.dialog({
        component: ServiceDialog,
        parent: this
      });
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
    protocolUpdated(newProtocol) {
      this.form.entrypoints = this.form.entrypoints.filter(({ protocol }) => {
        if (protocol == "tcp" && newProtocol == "http") {
          return true;
        }
        return protocol == newProtocol;
      });

      this.form.service = null;
    },
    validateRule(rule) {
      if (!this.$api.traefik.isValidRule(rule)) {
        return `Syntax error`;
      }
    }
  }
};
</script>
