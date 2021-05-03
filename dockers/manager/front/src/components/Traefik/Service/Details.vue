<template>
  <BaseDetails :errors="service.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section class="row q-gutter-sm items-center">
            <div class="col col-auto">
              <protocol-badge :protocol="service.protocol" />
            </div>
            <div class="text-h6 col">
              {{ service.name }}
            </div>
            <div class="col col-auto">
              {{ service.type }}
            </div>
          </q-card-section>
          <q-card-section>
            
            <create-service :value="service"/>
            <!-- 
            <create-http-load-balancer
              v-model="service.loadBalancer"
              v-if="
                service.protocol == 'http' && service.type == 'loadBalancer'
              "
            />
            <create-http-mirroring
              v-model="service.mirroring"
              v-if="service.protocol == 'http' && service.type == 'mirroring'"
            />
            <create-http-weighted
              v-model="service.weighted"
              v-if="service.protocol == 'http' && service.type == 'weighted'"
            />

            <create-tcp-load-balancer
              v-model="service.loadBalancer"
              v-if="service.protocol == 'tcp' && service.type == 'loadBalancer'"
            />
            <create-tcp-weighted
              v-model="service.weighted"
              v-if="service.protocol == 'tcp' && service.type == 'weighted'"
            />

            <create-udp-load-balancer
              v-model="service.loadBalancer"
              v-if="service.protocol == 'udp' && service.type == 'loadBalancer'"
            />
            <create-udp-weighted
              v-model="service.weighted"
              v-if="service.protocol == 'udp' && service.type == 'weighted'"
            /> -->
          </q-card-section>
        </q-card>
      </div>
    </template>
  </BaseDetails>
</template>

<script>
import CreateService from "./Create.vue"
import CreateHttpLoadBalancer from "./CreateHttpLoadBalancer.vue";
import CreateHttpMirroring from "./CreateHttpMirroring.vue";
import CreateHttpWeighted from "./CreateHttpWeighted.vue";
import CreateTcpLoadBalancer from "./CreateTcpLoadBalancer.vue";
import CreateTcpWeighted from "./CreateTcpWeighted.vue";
import CreateUdpLoadBalancer from "./CreateUdpLoadBalancer.vue";
import CreateUdpWeighted from "./CreateUdpWeighted.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
import ProtocolBadge from "../ProtocolBadge.vue";
export default {
  components: {
    CreateService,
    /* 
    CreateHttpLoadBalancer,
    CreateHttpMirroring,
    CreateHttpWeighted,
    CreateTcpLoadBalancer,
    CreateTcpWeighted,
    CreateUdpLoadBalancer,
    CreateUdpWeighted, */
    BaseDetails,
    ProtocolBadge
  },
  props: {
    service: { type: Object, required: true }
  },
  data() {
    return {};
  },
  methods: {
    serviceModified() {
      this.$emit("modified");
    }
  }
};
</script>
