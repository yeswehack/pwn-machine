<template>
  <base-table
    ref="table"
    name="container"
    row-key="id"
    :loading="$apollo.loading"
    :data="containers"
    :columns="columns"
    @clone="cloneContainer"
    @create="createContainer"
    @delete="deleteContainer"
  >
    <template #body-cell-image="{row}">
      <image-link :name="row.image.name" />
    </template>
    <template #body-cell-name="{value, row}">
      {{ value }}
      <q-badge
        rounded
        color="red"
        align="top"
        v-if="row.privileged"
        title="Privileged"
        class="q-ml-xs"
      />
    </template>
    <template #body-cell-volumes="{row}">
      <div class="q-gutter-sm">
        <volume-link
          :name="name"
          :key="name"
          v-for="{ volume: { name } } of row.mounts.filter(n => n.volume)"
        />
      </div>
    </template>
    <template #body-cell-networks="{row}">
      <div class="row q-gutter-sm">
        <network-link
          :name="connection.network.name"
          :key="idx"
          v-for="(connection, idx) of row.connections"
        >
          <q-tooltip
            v-if="connection.ipAddress"
            anchor="top middle"
            self="bottom middle"
            >{{ connection.ipAddress }}</q-tooltip
          >
        </network-link>
      </div>
    </template>
    <template #body-cell-ports="{row}">
      <port-list :ports="row.ports" />
    </template>
    <template #body-cell-status="{row}">
      <container-status :status="row.status" />
    </template>

    <template #details="{ row }" auto-width>
      <container-details :container="row" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ContainerDetails from "src/components/Docker/Container/Details.vue";
import PortList from "src/components/Docker/Container/PortList.vue";
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import ContainerDialog from "src/components/Docker/Container/Dialog.vue";
import CreateContainer from "src/components/Docker/Container/Create.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import VolumeLink from "src/components/Docker/Volume/Link.vue";
import NetworkLink from "src/components/Docker/Network/Link.vue";
import { mapGetters } from "vuex";
import { shortDate, shortName } from "src/utils";
import { quote } from "shell-quote";
import api from "src/api";

export default {
  components: {
    ContainerDetails,
    BaseTable,
    PortList,
    ContainerStatus,
    ImageLink,
    VolumeLink,
    NetworkLink
  },
  apollo: {
    containers: {
      query: api.docker.GET_CONTAINERS,
      update: ({ dockerContainers }) => dockerContainers
    }
  },
  data() {
    const col = (name, opts = {}) => ({
      name,
      align: "left",
      label: name,
      field: name,
      sortable: true,
      ...opts
    });
    const columns = [
      col("name"),
      col("image"),
      col("volumes"),
      col("networks"),
      col("ports", { label: "exposed ports" }),
      col("status")
    ];
    return { columns };
  },
  methods: {
    createContainer() {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this
      });
    },
    deleteContainer(container) {},
    cloneContainer(container) {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this,
        container
      });
    }
  }
};
</script>
