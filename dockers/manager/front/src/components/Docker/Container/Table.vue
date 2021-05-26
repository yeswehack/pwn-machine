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
      <q-item v-close-popup clickable @click="exposeContainer(row)">
        <q-item-section avatar>
          <q-avatar icon="eva-globe-outline" />
        </q-item-section>
        <q-item-section>Expose via traefik ...</q-item-section>
      </q-item>
    </template>
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
import ContainerStatus from "src/components/Docker/Container/Status.vue";
import ContainerDialog from "src/components/Docker/Container/Dialog.vue";
import ImageLink from "src/components/Docker/Image/Link.vue";
import VolumeLink from "src/components/Docker/Volume/Link.vue";
import NetworkLink from "src/components/Docker/Network/Link.vue";
import ExposeContainerDialog from "src/components/Docker/Container/ExposeContainerDialog.vue";
import api from "src/api";
import { format } from "quasar";
const { humanStorageSize } = format;

export default {
  components: {
    ContainerDetails,
    BaseTable,
    ContainerStatus,
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
          this.$apollo
            .mutate({
              mutation: api.docker.containers.PRUNE_CONTAINERS,
              refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
            })
            .then(({ data }) => {
              const deleted = data.pruneDockerContainers.deleted;
              const reclaimed = humanStorageSize(
                data.pruneDockerContainers.spaceReclaimed
              );
              const message = deleted.length
                ? `${deleted.length} container${deleted.length > 1 ? 's' : ''} deleted (${reclaimed})`
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
    deleteContainer(container) {},
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
        containerId: container.id,
      });
    }
  }
};
</script>
