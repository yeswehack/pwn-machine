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
            <div class="col" v-if="form.exposedPort.protocol == 'HTTP'">
              <q-select
                label="Domain"
                ref="domainSelect"
                input-debounce="0"
                use-input
                clearable
                :rules="[required]"
                new-value-mode="add"
                :options="domainOptions"
                v-model="form.domain"
                @input="onDomainInput"
                @filter="onFilter"
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
          <q-separator class="q-mx-xl q-mb-md"/>
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
          <q-separator class="q-mx-xl q-mb-md"/>
          <component
            ref="router"
            :is="routerComponent"
            v-model="form.routerForm"
          />
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
import DeepForm, { mapGetter } from "src/mixins/DeepForm";
import api from "src/api";

import CreateHTTPRouter from "src/components/Traefik/Router/CreateHTTP.vue";
import CreateTCPRouter from "src/components/Traefik/Router/CreateUDP.vue";
import CreateUDPRouter from "src/components/Traefik/Router/CreateTCP.vue";
import CreateHttpLoadBalancer from "src/components/Traefik/Service/CreateHttpLoadBalancer.vue";
import CreateUdpLoadBalancer from "src/components/Traefik/Service/CreateUdpLoadBalancer.vue";
import CreateTcpLoadBalancer from "src/components/Traefik/Service/CreateTcpLoadBalancer.vue";

import CheckTraefikConnection from "./CheckTraefikConnection.vue";
import ExposedPortInput from "./Form/ExposedPortInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";

function getRouterComponent(f) {
  const protocol = f?.exposedPort?.protocol;
  if (protocol == "UDP") {
    return CreateUDPRouter;
  }
  if (protocol == "TCP") {
    return CreateTCPRouter;
  }
  if (protocol == "HTTP") {
    return CreateHTTPRouter;
  }
  return null;
}
function getServiceComponent(f) {
  const protocol = f?.exposedPort?.protocol;
  if (protocol == "UDP") {
    return CreateUdpLoadBalancer;
  }
  if (protocol == "TCP") {
    return CreateTcpLoadBalancer;
  }
  if (protocol == "HTTP") {
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
    dnsRules: {
      query: api.dns.GET_RULES
    },
    container: {
      query: api.docker.container.GET_CONTAINER_BY_ID,
      variables() {
        return { id: this.containerId };
      },
      update: data => data.dockerContainerById
    }
  },
  data() {
    return {
      step: 1,
      panel: "choosePort",
      currentDomain: null,
      needle: ""
    };
  },
  computed: {
    ...mapGetter(
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
        "serviceName"
      ];
      return steps;
    },
    portOptions() {
      return (this.container?.ports ?? [])
        .filter(p => p.protocol == "TCP")
        .map(p => p.containerPort);
    },
    domainOptions() {
      return (this.dnsRules ?? [])
        .filter(r => ["A", "AAAA", "CNAME"].includes(r.type))
        .map(r => r.name.slice(0, -1))
        .filter(name => name.includes(this.needle));
    }
  },
  methods: {
    validateServiceName(v) {
      if (!v) return "Please enter a valid service name.";
    },
    validateRouterName(v) {
      if (!v) return "Please enter a valid routter name.";
    },
    onFilter(v, done) {
      done(() => {
        this.needle = (v ?? "").toLowerCase();
      });
    },
    required(v) {
      if (!v) {
        return "This field is required";
      }
    },
    onDomainInput(domain) {
      if (domain && domain.startsWith("*")) {
        const el = this.$refs.domainSelect.$el;
        const input = el.querySelector(".q-field__input");
        this.$refs.domainSelect.updateInputValue(domain.slice(1), false);
        el.blur();
        this.$nextTick(() => {
          this.form.domain = null;
          input.setSelectionRange(0, 0);
          input.focus();
        });
      }
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
