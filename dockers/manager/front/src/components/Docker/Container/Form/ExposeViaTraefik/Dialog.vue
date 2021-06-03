<template>
  <base-dialog
    ref="dialog"
    title="Expose via traefik"
    :subtitle="panel"
    :loading="$apollo.loading"
  >
    <template #default="{ok, cancel}">
      <q-tab-panels v-model="panel" animated>
        <q-tab-panel name="choosePort">
          <div class="column q-col-gutter-sm">
            <div class="col">
              <component
                ref="exposedPort"
                :is="formChildren.exposedPort"
                v-model="form.exposedPort"
                :container="container"
              />
            </div>
            <div class="col" v-if="form.exposedPort.protocol == 'http'">
              <component :is="formChildren.domain" v-model="form.domain" />
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
          <div class="row items-baseline">
            <div class="col text-h6">New service:</div>
            <div class="col col-5">
              <q-input
                ref="serviceName"
                filled
                :rules="[validateServiceName]"
                v-model="form.serviceName"
                label="name"
              />
            </div>
          </div>
          <q-separator class="q-mx-xl q-mb-md" />
          <component
            ref="service"
            :is="serviceComponent"
            v-model="form.serviceForm"
          />
        </q-tab-panel>
        <q-tab-panel name="createRouter">
          <div class="row items-baseline">
            <div class="col text-h6">New router:</div>
            <div class="col col-5">
              <q-input
                ref="routerName"
                filled
                :rules="[validateRouterName]"
                v-model="form.routerName"
                label="name"
              />
            </div>
          </div>
          <q-separator class="q-mx-xl q-mb-md" />
          <component
            ref="router"
            :is="routerComponent"
            v-model="form.routerForm"
          />
        </q-tab-panel>
        <q-tab-panel name="create" class="q-gutter-sm">
          <div class="row text-h6">
            Summary
          </div>
          <div class="row">
            <div class="col">
              Expose port {{ form.exposedPort.port }}/{{
                form.exposedPort.protocol
              }}
            </div>
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
      <div :value="container" @ok="ok" @cancel="cancel" v-if="0">
        {{ container }}
      </div>
    </template>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import DeepForm, { mapGetters } from "src/mixins/DeepForm";
import api from "src/api";

import CreateHTTPRouter from "src/components/Traefik/Router/CreateHTTP.vue";
import CreateTCPRouter from "src/components/Traefik/Router/CreateUDP.vue";
import CreateUDPRouter from "src/components/Traefik/Router/CreateTCP.vue";
import CreateHttpLoadBalancer from "src/components/Traefik/Service/CreateHttpLoadBalancer.vue";
import CreateUdpLoadBalancer from "src/components/Traefik/Service/CreateUdpLoadBalancer.vue";
import CreateTcpLoadBalancer from "src/components/Traefik/Service/CreateTcpLoadBalancer.vue";

import CheckTraefikConnection from "./CheckTraefikConnection.vue";
import ExposedPortInput from "./ExposedPortInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import { notify } from "src/utils";
import DomainInput from "src/components/DNS/DomainInput.vue";

function getRouterComponent(f) {
  const protocol = f?.exposedPort?.protocol;
  if (protocol == "udp") {
    return CreateUDPRouter;
  }
  if (protocol == "tcp") {
    return CreateTCPRouter;
  }
  if (protocol == "http") {
    return CreateHTTPRouter;
  }
  return null;
}
function getServiceComponent(f) {
  const protocol = f?.exposedPort?.protocol;
  if (protocol == "udp") {
    return CreateUdpLoadBalancer;
  }
  if (protocol == "tcp") {
    return CreateTcpLoadBalancer;
  }
  if (protocol == "http") {
    return CreateHttpLoadBalancer;
  }
  return null;
}

export default {
  components: { BaseDialog, ResetAndSave, CheckTraefikConnection },
  mixins: [DeepForm],
  formDefinition: {
    serviceName: null,
    routerName: null,
    exposedPort: ExposedPortInput,
    aliasName: null,
    domain: DomainInput,
    routerForm(f) {
      return getRouterComponent(f);
    },
    serviceForm(f) {
      return getServiceComponent(f);
    }
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
  data() {
    return {
      step: 1,
      panel: "choosePort"
    };
  },
  computed: {
    ...mapGetters(
      "exposedPort.port",
      "exposedPort.protocol",
      "serviceForm.name",
      "domain",
      "serviceName",
      "routerName",
      "aliasName"
    ),
    routerComponent() {
      return getRouterComponent(this.form);
    },
    serviceComponent() {
      return getServiceComponent(this.form);
    },
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
        .filter(p => p.protocol == "TCP")
        .map(p => p.containerPort);
    }
  },
  methods: {
    validateServiceName(v) {
      if (!v) return "Please enter a valid service name.";
    },
    validateRouterName(v) {
      if (!v) return "Please enter a valid routter name.";
    },
    required(v) {
      if (!v) {
        return "This field is required";
      }
    },
    submit() {
      const protocol = this.form.exposedPort.protocol;
      const serviceMutation =
        api.traefik.services.CREATE_SERVICE[protocol].loadBalancer;
      const serviceInput = {
        name: this.form.serviceName,
        loadBalancer: this.form.serviceForm
      };
      const routerMutation = api.traefik.routers.CREATE_ROUTER[protocol];

      const routerInput = {
        name: this.form.routerName,
        ...this.form.routerForm
      };
      this.mutate({
        mutation: serviceMutation,
        variables: { input: serviceInput },
        message: `Service ${this.form.serviceName} created.`
      }).then(r => {
        return this.mutate({
            mutation: routerMutation,
            variables: { input: routerInput },
            message: `Router ${this.form.routerName} created.`
          })
      });
    },
    updateRouterDefault() {
      if (!this.form.routerForm) return;
      this.form.routerForm.rule = `Host(\`${this.domain}\`) && PathPrefix(\`/\`)`;
      this.form.routerForm.service = this.serviceName;
    },
    updateServiceDefault() {
      if (!this.form.serviceForm) return;
      this.form.serviceForm.servers = [
        { url: `http://${this.aliasName}:${this.exposedPort_port}` }
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
    routerComponent: {
      immediate: true,
      handler() {
        this.updateRouterDefault();
      }
    },
    serviceComponent: {
      immediate: true,
      handler() {
        this.updateServiceDefault();
      }
    },
    serviceName() {
      this.updateRouterDefault();
    },
    aliasName() {
      this.updateServiceDefault();
    },
    exposedPort_port() {
      this.updateServiceDefault();
    },
    exposedPort_protocol(protocol) {
      const serviceComponent = this.instanciateSubForm(
        getServiceComponent(this.form),
        this.form
      );
      this.form.serviceForm = serviceComponent.originalForm;

      const routerComponent = this.instanciateSubForm(
        getRouterComponent(this.form),
        this.form
      );
      this.form.routerForm = routerComponent.originalForm;
      this.updateServiceDefault();
    }
  }
};
</script>

<style></style>
