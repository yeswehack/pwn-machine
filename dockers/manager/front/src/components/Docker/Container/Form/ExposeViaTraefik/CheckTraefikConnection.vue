<template>
  <div class="column q-gutter-md">
    <div class="col row justify-between items-center">
      <div class="col text-h6 ">
        Connection to traefik
      </div>
      <div class="col col-auto">
        <q-badge
          :label="this.isConnected ? 'Connected' : 'Disconnected'"
          :color="this.isConnected ? 'positive' : 'negative'"
        />
      </div>
    </div>
    <template v-if="isConnected">
      <div class="col text-negative" v-show="invalid">
        Please make a selection
      </div>
      <div class="col">
        Choose the IP or hostname to use
        <q-tree
          default-expand-all
          :nodes="commonNetworks"
          node-key="id"
          class="q-mt-sm"
        >
          <template v-slot:header-alias="prop">
            <div class="row items-center">
              <div class="col">
                <q-radio
                  v-model="form"
                  :label="prop.node.label"
                  :val="prop.node.label"
                />
              </div>
            </div>
          </template>
        </q-tree>
      </div>
    </template>
    <template v-else>
      <div class="col text-negative" v-show="invalid">
        Please connect your container to traefik
      </div>
      <div class="col">
        <q-select
          v-model="connectTo"
          label="Connect to one of traefik networks"
          :options="traefikNetworkOptions"
        >
          <template #after>
            <q-btn
              :disable="!connectTo"
              label="Connect"
              color="positive"
              @click.stop="connectToNetwork"
            />
          </template>
        </q-select>
      </div>

      <div class="col row col-auto q-gutter-md items-center">
        <div class="col-auto">
          Or
        </div>
        <div class="col">
          <q-btn
            label="Create a new network"
            color="positive"
            @click="createNetwork"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import NetworkDialog from "src/components/Docker/Network/Dialog.vue";
export default {
  mixins: [DeepForm],
  formDefinition: null,
  components: {},
  props: {
    container: { type: Object, required: true }
  },
  apollo: {
    traefikContainer: {
      query: api.docker.containers.GET_CONTAINER_BY_NAME,
      variables: { name: "pm_traefik" },
      update: data => data.dockerContainerByName
    }
  },
  data() {
    return { connectTo: null, invalid: false };
  },
  methods: {
    validate() {
      this.invalid = !this.form;
      return !this.invalid;
    },
    connectToNetwork() {
      const input = {
        containerId: this.container.id,
        networkId: this.connectTo.value,
        aliases: [this.container.name]
      };
      this.mutate({
        mutation: api.docker.networks.CONNECT_TO_NETWORK,
        variables: { input },
        refetchQueries: [
          {
            query: api.docker.containers.GET_CONTAINER_BY_ID,
            variables: { id: this.container.id }
          }
        ]
      });
    },
    createNetwork() {
      const connectContainer = (container, networkId, refetchQueries = []) => {
        const input = {
          containerId: container.id,
          networkId,
          aliases: [container.name]
        };
        return this.mutate({
          mutation: api.docker.networks.CONNECT_TO_NETWORK,
          variables: { input },
          refetchQueries
        });
      };

      this.$q
        .dialog({
          component: NetworkDialog,
          parent: this
        })
        .onOk(async network => {
          await connectContainer(this.container, network);
          await connectContainer(this.traefikContainer, network, [
            {
              query: api.docker.containers.GET_CONTAINER_BY_ID,
              variables: { id: this.container.id }
            }
          ]);
          await this.$apollo.queries.traefikContainer.refetch();
        });
    }
  },
  computed: {
    traefikConnections() {
      return (this.traefikContainer?.connections ?? []).reduce((acc, co) => {
        return { ...acc, [co.network.name]: co };
      }, {});
    },
    isConnected() {
      return !!Object.keys(this.commonNetworks).length;
    },
    traefikNetworkOptions() {
      const options = [];
      for (const [name, connection] of Object.entries(
        this.traefikConnections
      )) {
        options.push({
          label: name,
          value: connection.network.id
        });
      }
      return options;
    },
    commonNetworks() {
      const networks = [];
      for (const connection of this.container.connections) {
        const name = connection.network.name;
        if (!(name in this.traefikConnections)) {
          continue;
        }

        const children = connection.aliases.map(alias => ({
          label: alias,
          header: "alias",
          id: `n-${name}-${alias}`
        }));
        children.unshift({
          label: connection.ipAddress,
          header: "alias",
          id: `n-${name}-${connection.ipAddress}`
        });
        networks.push({
          icon: "eva-globe-outline",
          label: name,
          id: `n-${name}`,
          children
        });
      }
      return networks;
    }
  }
};
</script>

<style></style>
