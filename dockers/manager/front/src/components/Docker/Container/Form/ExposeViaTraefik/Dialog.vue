<template>
  <base-dialog
    ref="dialog"
    title="Expose via traefik"
    :subtitle="panel"
    :loading="$apollo.loading"
  >
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="choosePort">
        <div class="column q-col-gutter-sm">
          <div class="col">
            <component
              ref="exposedPort"
              :is="formChildren.exposedPort"
              v-model="form.exposedPort"
              protocol="http"
              :container="container"
            />
          </div>
          <div class="col">
            <component
              :is="formChildren.domain"
              ref="domainSelect"
              v-model="form.domain"
            />
          </div>
        </div>
      </q-tab-panel>
      <q-tab-panel name="checkTraefikConnection">
        <check-traefik-connection
          :container="container"
          ref="aliasName"
          v-model="form.aliasName"
        />
      </q-tab-panel>
      <q-tab-panel name="createService">
        <q-input
          ref="serviceName"
          :rules="[required('Please enter a valid service name.')]"
          v-model="form.serviceName"
          label="name"
        />
        <component
          ref="service"
          :is="formChildren.serviceForm"
          v-model="form.serviceForm"
        />
      </q-tab-panel>
      <q-tab-panel name="createRouter">
        <q-input
          ref="routerName"
          :rules="[required('Please enter a valid router name.')]"
          v-model="form.routerName"
          label="name"
        />
        <component
          ref="router"
          :is="formChildren.routerForm"
          v-model="form.routerForm"
        />
      </q-tab-panel>
      <q-tab-panel name="create" class="q-gutter-sm">
        <div class="row text-h6">
          Summary
        </div>
        <div class="row">
          <div class="col">Expose port {{ form.exposedPort }}</div>
        </div>
        <div class="row">
          <div class="col">Create service {{ form.serviceName }}</div>
          <div class="col col-auto">
            <q-icon name="close" />
          </div>
        </div>
        <div class="row">
          <div class="col">Create router {{ form.routerName }}</div>
          <div class="col col-auto">
            <q-icon name="close" />
          </div>
        </div>
      </q-tab-panel>
    </q-tab-panels>
    <q-card-section>
      <reset-and-save
        :steps="steps"
        :step.sync="panel"
        :modified="modified"
        @save="submit"
        @reset="reset"
      />
    </q-card-section>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import DeepForm, { mapGetters } from "src/mixins/DeepForm";
import api from "src/api";

import CreateHTTPRouter from "src/components/Traefik/Router/CreateHTTP.vue";
import CreateHttpLoadBalancer from "src/components/Traefik/Service/CreateHttpLoadBalancer.vue";

import CheckTraefikConnection from "./CheckTraefikConnection.vue";
import ExposedPortInput from "./ExposedPortInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import DomainInput from "src/components/DNS/DomainInput.vue";

export default {
  components: { BaseDialog, ResetAndSave, CheckTraefikConnection },
  mixins: [DeepForm],
  formDefinition: {
    serviceName: null,
    routerName: null,
    exposedPort: ExposedPortInput,
    aliasName: null,
    domain: DomainInput,
    routerForm: CreateHTTPRouter,
    serviceForm: CreateHttpLoadBalancer
  },
  props: {
    containerId: { type: String, required: true }
  },
  apollo: {
    container: {
      query: api.docker.containers.GET_CONTAINER_BY_ID,
      variables() {
        return { id: this.containerId };
      },
      update: data => data.dockerContainerById
    }
  },
  data: () => ({ step: 1, panel: "choosePort" }),
  computed: {
    ...mapGetters(
      "exposedPort",
      "serviceForm.name",
      "domain",
      "serviceName",
      "routerName",
      "aliasName"
    ),
    steps() {
      const steps = [
        {
          name: "choosePort",
          validate: () => {
            return [
              this.$refs.exposedPort.validate(),
              this.$refs.domainSelect.validate()
            ].every(x => x);
          }
        },
        {
          name: "checkTraefikConnection",
          validate: () => {
            return this.$refs.aliasName.validate();
          }
        },
        {
          name: "createService",
          validate: () => {
            const validators = [
              this.$refs.serviceName.validate(),
              this.$refs.service.validate()
            ];
            return validators.every(x => x);
          }
        },
        {
          name: "createRouter",
          validate: () => {
            const validators = [
              this.$refs.routerName.validate(),
              this.$refs.router.validate()
            ];
            return validators.every(x => x);
          }
        },
        "create"
      ];
      return steps;
    },
    portOptions() {
      return (this.container?.ports ?? [])
        .filter(p => p.protocol === "TCP")
        .map(p => p.containerPort);
    }
  },
  methods: {
    submit(done) {
      const serviceMutation =
        api.traefik.services.CREATE_SERVICE.http.loadBalancer;
      const serviceInput = {
        name: this.form.serviceName,
        loadBalancer: this.form.serviceForm
      };
      const routerMutation = api.traefik.routers.CREATE_ROUTER.http;

      const routerInput = {
        name: this.form.routerName,
        ...this.form.routerForm
      };
      routerInput.service = `${routerInput.service}@redis`;

      this.mutate({
        mutation: serviceMutation,
        variables: { input: serviceInput },
        message: `Service ${this.form.serviceName} created.`
      })
        .then(() => {
          return this.mutate({
            mutation: routerMutation,
            variables: { input: routerInput },
            message: `Router ${this.form.routerName} created.`
          }).then(() => {
            this.$refs.dialog.onOk();
          });
        })
        .finally(done);
    },
    updateRouterDefault() {
      if (!this.form.routerForm) return;
      this.form.routerForm.rule = `Host(\`${this.domain}\`) && PathPrefix(\`/\`)`;
      this.form.routerForm.service = this.serviceName;
    },
    updateServiceDefault() {
      if (!this.form.serviceForm) return;
      this.form.serviceForm.servers = [
        { url: `http://${this.aliasName}:${this.exposedPort}` }
      ];
    },
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    }
  },
  watch: {
    container() {
      this.form.serviceName = `${this.container.name}-service`;
      this.form.routerName = `${this.container.name}-router`;
    },
    serviceName() {
      this.updateRouterDefault();
    },
    domain() {
      this.updateRouterDefault();
    },
    aliasName() {
      this.updateServiceDefault();
    },
    exposedPort() {
      this.updateServiceDefault();
    }
  }
};
</script>
