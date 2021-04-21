<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card bordered style="min-width: 600px">
      <q-form @submit="createRouter">
        <q-card-section>
          <div class="row items-center">
            <div class="text-h6">Create a new router</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </div>
        </q-card-section>
        <q-separator />
        <q-card-section class="q-gutter-sm">
          <q-input v-model="form.name" autofocus required label="Name" />
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
            :disable="!this.form.protocol"
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
            :disable="!this.form.protocol"
            multiple
            use-chips
            :rules="[nonEmptyArray]"
            :options="relevantentrypoints"
            label="entrypoints"
          />

          <q-select
            :disable="!this.form.protocol"
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
          <q-btn color="warning" label="Cancel" @click="onCancelClick" />
          <q-btn
            color="positive"
            type="submit"
            label="Create"
            @click="createRouter"
          />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
import db from "src/gql";
import ServiceDialog from "../Service/Dialog.vue";
export default {
  props: {
    router: { type: Object, default: null }
  },
  apollo: {
    entrypoints: {
      query: db.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    },
    services: {
      query: db.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
  },
  data() {
    const form = {
      name: this.router?.name,
      protocol: this.router?.protocol || "http",
      rule: this.router?.rule,
      entrypoints: this.router?.entryPoints || [],
      service: this.router?.service?.name
    };
    const protocols = ["http", "tcp", "udp"];
    return { form, protocols };
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
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    onDialogHide() {
      this.$emit("hide");
    },
    onOKClick() {
      this.$emit("ok");
      this.hide();
    },
    onCancelClick() {
      this.hide();
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
    },
    createService() {
      this.$q.dialog({
        component: ServiceDialog,
        parent: this
      });
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
          mutation: db.traefik.CREATE_ROUTER,
          variables: { input },
          refetchQueries: [{ query: db.traefik.GET_ROUTERS }]
        })
        .then(r => {
          this.hide();
        });
    }
  }
};
</script>
