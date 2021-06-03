<template>
  <base-table
    name="volume"
    row-key="name"
    :expendable="true"
    :query="$apollo.queries.volumes"
    :data="volumes"
    :columns="columns"
    no-details
    @create="createVolume"
    @clone="cloneVolume"
    @delete="deleteVolume"
    @refresh="$apollo.queries.volumes.refetch"
  >
    <template #header-button>
      <q-btn
        rounded
        label="Prune"
        color="negative"
        icon="eva-trash-outline"
        @click="pruneVolumes"
      />
    </template>
    <template #body-cell-usedBy="{row}">
      <div class="q-gutter-sm row">
        <container-link
          :name="name"
          :key="name"
          v-for="{ name } of row.usedBy"
        />
      </div>
    </template>
  </base-table>
</template>

<script>
import BaseTable from "src/components/BaseTable.vue";
import ContainerDialog from "./Dialog.vue";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";
import { format } from "quasar";
import { notify } from "src/utils";
const { humanStorageSize } = format;

export default {
  components: { BaseTable, ContainerLink },
  apollo: {
    volumes: {
      query: api.docker.volumes.LIST_VOLUMES,
      update: data => data.dockerVolumes
    }
  },
  methods: {
    pruneVolumes() {
      this.$q
        .dialog({
          title: "Prune volumes ?",
          message:
            "This will remove all volumes not used by at least one container.",
          color: "negative",
          type: "confirm",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.volumes.PRUNE_VOLUMES,
            refetchQueries: [{ query: api.docker.volumes.LIST_VOLUMES }]
          }).then(result => {
            const deleted = result.deleted;
            const reclaimed = humanStorageSize(result.spaceReclaimed);
            const message = deleted.length
              ? `${deleted.length} volume(s) deleted: ${deleted.join(
                  ", "
                )} (${reclaimed})`
              : `No volume deleted.`;

            this.$q.notify({
              message,
              type: "positive"
            });
          });
        });
    },
    createVolume() {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this
      });
    },
    cloneVolume(volume) {
      this.$q.dialog({
        component: ContainerDialog,
        parent: this,
        volume
      });
    },
    deleteVolume(volume) {
      this.$q
        .dialog({
          title: "Confirm",
          message: `Are you sure you want to delete ${volume.name}?`,
          color: "negative",
          cancel: true
        })
        .onOk(() => {
          this.mutate({
            mutation: api.docker.volumes.DELETE_VOLUME,
            variables: { name: volume.name },
            refetchQueries: [{ query: api.docker.volumes.LIST_VOLUMES }],
            message: `Volume ${volume.name} deleted.`
          });
        });
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
      col("path", { field: "mountpoint" }),
      col("usedBy", {
        label: "used by",
        field: "usedBy"
      })
    ];
    return { columns };
  }
};
</script>
