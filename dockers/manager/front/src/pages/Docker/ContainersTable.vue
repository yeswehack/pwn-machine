<template>
  <BaseTable
    ref="table"
    name="container"
    rkey="name"
    :loading="$apollo.loading"
    :data="containers"
    :columns="columns"
    v-on:cloneRow="cloneContainer"
    v-on:newRow="newContainer"
    v-on:delete="deleteContainer"
  >
    <template #body-cell-image="{row}">
      <ImageLink :name="row.image.repository" />
    </template>
    <template #body-cell-volumes="{row}">
      <div class="q-gutter-sm">
        <VolumeLink :name="name" :key="name" v-for="{ name } of row.mounts.filter(n=>n.name)" />
      </div>
    </template>
    <template #body-cell-networks="{row}">
      <div class="q-gutter-sm">
        <NetworkLink
          :name="name"
          :key="name"
          v-for="{ name } of row.connectedNetworks"
        />
      </div>
    </template>
    <template #body-cell-exposedPort="{row}">
      <PortList :ports="row.exposedPorts" />
    </template>
    <template #body-cell-status="{row}">
      <ContainerStatus :status="row.status" />
    </template>

    <template #details="{ row }" auto-width>
      <ContainerDetails :name="row.name" />
    </template>

    <template #popup>
      <CreateContainer v-on:submit="createContainer" v-model="containerForm" />
    </template>
  </BaseTable>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ContainerDetails from "src/components/Docker/Container/Details.vue";
import PortList from "src/components/Docker/Container/PortList.vue";
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import CreateContainer from "src/components/Docker/Container/Create.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import VolumeLink from "src/components/Docker/Volume/Link.vue";
import NetworkLink from "src/components/Docker/Network/Link.vue";
import { mapGetters } from "vuex";
import { shortDate, shortName } from "src/utils";
import { quote } from "shell-quote";

import graphql from "src/gql/docker"

const {queries: {getDockerContainers}} = graphql;

export default {
  components: {
    ContainerDetails,
    BaseTable,
    PortList,
    CreateContainer,
    ContainerStatus,
    ImageLink,
    VolumeLink,
    NetworkLink
  },
  apollo: {
    containers: {
      query: getDockerContainers,
      update: data => data.docker.containers
    }
  },
  computed: mapGetters(["loading"]),
  data() {
    const columns = [
      {
        name: "name",
        align: "left",
        label: "name",
        field: "name",
        sortable: true
      },
      {
        name: "image",
        label: "Image",
        align: "left",
        field: row => row.image.repository,
        sortable: true
      },
      {
        name: "volumes",
        label: "Volumes",
        align: "left",
        field: row => row.volumeMounts.map(m => m.name),
        format: val => shortDate(val),
        sortable: true
      },
      {
        name: "networks",
        label: "Networks",
        align: "left",
        field: row => row.connectedNetworks.map(n => n.name),
        sortable: true
      },
      {
        name: "exposedPort",
        label: "Exposed ports",
        align: "left",
        field: row => row.exposedPorts.map(e => e.protocol + e.containerPort),
        sortable: true
      },
      {
        name: "status",
        label: "Status",
        align: "left",
        field: row => row.status,
        sortable: true
      }
    ];
    const containerForm = this.emptyContainer();
    return { containerForm, columns };
  },
  methods: {
    createContainer(f) {
      const postData = {};
      const restartPolicy = {};
      const hostConfig = {};
      const setIfNotNull = (obj, key, val) => {
        if (val === null) return;
        if (Array.isArray(val) && val.length === 0) return;
        if (val.constructor === String && val.length === 0) return;
        if (val.constructor === Object && Object.keys(val).length == 0) return;
        obj[key] = val;
      };

      setIfNotNull(postData, "Image", f.image);
      setIfNotNull(postData, "Cmd", f.extra.cmd);
      setIfNotNull(postData, "User", f.extra.user);
      console.log(f.env);
      setIfNotNull(
        postData,
        "Env",
        Object.entries(f.env).map(([name, v]) => `${name}=${v}`)
      );
      setIfNotNull(postData, "Labels", f.labels);

      setIfNotNull(restartPolicy, "Name", f.extra.restartPolicy);

      setIfNotNull(hostConfig, "RestartPolicy ", restartPolicy);
      setIfNotNull(hostConfig, "Capabilities", f.extra.capabilities);
      setIfNotNull(postData, "HostConfig ", hostConfig);

      console.log("submit", postData);
    },
    deleteContainer() {},
    newContainer() {
      this.containerForm = this.emptyContainer();
    },
    cloneContainer(container) {
      this.containerForm = this.containerToForm(container);
    },
    emptyContainer() {
      return {
        extra: {
          cmd: null,
          user: null,
          restartPolicy: null,
          capabilities: []
        },
        env: {},
        labels: {},
        network: {
          ports: [],
          networks: []
        },
        volumes: [],
        image: "",
        name: "",
        start: true,
        rm: false
      };
    },
    containerToForm(container) {
      const networks = Object.keys(container.NetworkSettings.Networks);
      const ports = Object.entries(container.NetworkSettings.Ports)
        .filter(([k, v]) => v != null)
        .map(([k, v]) => {
          return {
            host: v[0].HostPort,
            container: k.split("/")[0],
            protocol: k.split("/")[1]
          };
        });
      const env = container.Config.Env.reduce((acc, s) => {
        const [k, v] = s.split(/=(.+)/, 2);
        return { ...acc, [k]: v };
      }, {});
      const volumes = container.Mounts.map(m => {
        return {
          type: m.Type,
          name: m.Type == "volume" ? shortName(m.Name) : m.Source,
          destination: m.Destination,
          rw: m.RW
        };
      });
      const cmd = Array.isArray(container.Config.Cmd)
        ? quote(container.Config.Cmd)
        : container.Config.Cmd;

      const restartPolicy = container.HostConfig.RestartPolicy
        ? container.HostConfig.RestartPolicy.Name
        : null;
      const form = {
        extra: {
          cmd,
          user: container.Config.User,
          restartPolicy,
          capabilities: []
        },
        env,
        labels: container.Config.Labels,
        network: {
          ports,
          networks
        },
        volumes,
        image: container.Config.Image,
        name: container.Name,
        start: true,
        rm: false
      };
      return form;
    }
  }
};
</script>
