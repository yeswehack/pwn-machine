<template>
  <base-table
    ref="table"
    name="container"
    row-key="name"
    :query="$apollo.queries.containers"
    :data="containers"
    :columns="columns"
    @clone="cloneContainer"
    @create="createContainer"
    @delete="deleteContainer"
  >
    <template #header-button>
      <q-btn
        rounded
        label="Prune"
        color="negative"
        icon="eva-trash-outline"
        @click="pruneContainers"
      />
    </template>
    <template #menu="{row}">
      <q-item v-close-popup clickable @click="openShell(row)">
        <q-item-section avatar>
          <q-avatar icon="navigate_next" />
        </q-item-section>
        <q-item-section>Start a shell ...</q-item-section>
      </q-item>
      <q-item v-close-popup clickable @click="exposeContainer(row)">
        <q-item-section avatar>
          <q-avatar icon="eva-globe-outline" />
        </q-item-section>
        <q-item-section>Expose via traefik ...</q-item-section>
      </q-item>
    </template>
    <template #body-cell-image="{row}">
      <image-link :image="row.image" />
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
          v-for="{ name } of row.mounts.filter(n => n.type == 'volume')"
        />
      </div>
    </template>
    <template #body-cell-networks="{row}">
      <div class="row q-gutter-sm">
        <template v-for="(connection, idx) of row.connections">
          <network-link :network="connection.network" :key="idx">
            <q-tooltip
              v-if="connection.ipAddress"
              anchor="top middle"
              self="bottom middle"
              >{{ connection.ipAddress }}</q-tooltip
            >
          </network-link>
        </template>
      </div>
    </template>
    <template #body-cell-status="{row}">
      <container-status :status="row.status" />
    </template>
    <template #body-cell-ports="{row}">
      <port-list :ports="row.ports" />
    </template>

    <template #details="{ row }" auto-width>
      <container-details :container="row" />
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ContainerDetails from "src/components/Docker/Container/Details.vue";
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import ContainerDialog from "src/components/Docker/Container/Dialog.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import VolumeLink from "src/components/Docker/Volume/Link.vue";
import PortList from "src/components/Docker/Container/PortList.vue";
import NetworkLink from "src/components/Docker/Network/Link.vue";
import ExposeContainerDialog from "src/components/Docker/Container/Form/ExposeViaTraefik/Dialog.vue";
import ShellDialog from "src/components/Shell/Dialog.vue";
import api from "src/api";
import { format } from "quasar";
const { humanStorageSize } = format;

export default {
  components: {
    ContainerDetails,
    BaseTable,
    ContainerStatus,
    PortList,
    ImageLink,
    VolumeLink,
    NetworkLink
  },
  apollo: {
    containers: {
      query: api.docker.containers.LIST_CONTAINERS,
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
      col("name", { autoWidth: true }),
      col("image"),
      col("volumes"),
      col("networks"),
      col("ports", { label: "exposed ports" }),
      col("status", { autoWidth: true })
    ];
    return { columns };
  },
  methods: {
    async openShell(container) {
      this.$q.dialog({
        component: ShellDialog,
        parent: this,
        container
      });
    },
    pruneContainers() {
      this.$q
        .dialog({
          title: "Prune containers ?",
          message: "This will remove all stopped containers.",
          color: "negative",
          type: "confirm",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.containers.PRUNE_CONTAINERS,
            refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
          }).then(result => {
            const deleted = result.deleted;
            const reclaimed = humanStorageSize(result.spaceReclaimed);
            const message = deleted.length
              ? `${deleted.length} container${
                  deleted.length > 1 ? "s" : ""
                } deleted (${reclaimed})`
              : `No container deleted.`;
            this.$q.notify({
              message,
              type: "positive"
            });
          });
        });
    },
    createContainer() {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this
      });
    },
    deleteContainer(container) {
      this.$q
        .dialog({
          title: "Confirm",
          options: {
            model: [],
            items: [
              {
                label: "Force the removal (uses SIGKILL)",
                value: "force",

                color: "primary"
              },
              {
                label: "Remove associated anonymous volumes ",
                value: "pruneVolumes",

                color: "primary"
              }
            ],
            type: "toggle"
          },
          message: `Are you sure you want to delete ${container.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(result => {
          const force = result.includes("force");
          const pruneVolumes = result.includes("pruneVolumes");
          this.mutate({
            mutation: api.docker.containers.DELETE_CONTAINER,
            variables: { id: container.id, force, pruneVolumes },
            refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }],
            message: `${container.name} deleted.`
          });
        });
    },
    cloneContainer(container) {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this,
        container
      });
    },
    exposeContainer(container) {
      this.$q.dialog({
        component: ExposeContainerDialog,
        parent: this,
        containerId: container.id
      });
    }
  }
};
</script>
