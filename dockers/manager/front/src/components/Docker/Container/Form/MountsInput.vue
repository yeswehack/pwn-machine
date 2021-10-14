<template>
  <q-expansion-item
    icon="eva-hard-drive-outline"
    label="Mounts"
    :caption="`${form.length} mount(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <component
          :is="formChildren"
          v-model="form"
          :default="{ type: 'volume', readonly: false }"
          :titles="['Type', 'Name/Source', 'Target', 'Read Only']"
          grid-format="85px 1fr 1fr auto"
          :readonly="readonly"
        >
          <template #type.noedit="props">
            <q-select
              v-model="props.model.type"
              :options="['volume', 'bind', 'tmpfs']"
              :rules="[required()]"
              label="Type"
              flat
              v-bind="props"
            />
          </template>

          <template #name="props">
            <q-select
              v-if="props.model.type === 'volume'"
              v-model="props.model.name"
              :options="volumeOptions"
              :rules="[required('Please select a volume')]"
              label="Name"
              flat
              v-bind="props"
            >
              <template #selected-item="{opt}">
                <div class="ellipsis">{{ opt }}</div>
              </template>
            </q-select>
          </template>
          <template #display-name="{name}">
            <volume-link v-if="name" :name="name" />
          </template>
          <template #source="props">
            <q-input
              v-if="props.model.type === 'bind'"
              v-model="props.model.source"
              :rules="[required('A bind mount must have a source')]"
              label="Source"
              flat
              v-bind="props"
            />
            <span v-else-if="props.model.type === 'tmpfs'" />
          </template>

          <template #target="props">
            <q-input
              v-model="props.model.target"
              :rules="[required('You must specify a mountpoint')]"
              label="Target"
              flat
              v-bind="props"
            />
          </template>
          <template #readonly.nopopup="props">
            <q-toggle
              v-model="props.model.readonly"
              checked-icon="lock"
              class="fit"
              v-bind="props"
            />
            <q-tooltip anchor="top middle" self="bottom middle">
              {{ props.model.readonly ? "Read only" : "Read/Write" }}
            </q-tooltip>
          </template>
        </component>
      </q-card-section>

      <q-card-section v-if="!readonly">
        <div class="row justify-end">
          <q-btn
            dense
            color="positive"
            icon="eva-plus"
            label="Create a new volume"
            @click="createVolume"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import api from "src/api";
import VolumeLink from "../../Volume/Link.vue";
import ListInput from "src/components/ListInput.vue";
import VolumeDialog from "../../Volume/Dialog.vue";

export default {
  components: { VolumeLink },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: ListInput,
  apollo: {
    dockerVolumes: {
      query: api.docker.volumes.LIST_VOLUMES
    }
  },
  computed: {
    volumeOptions() {
      return this.dockerVolumes?.map(v => v.name) ?? [];
    }
  },
  methods: {
    createVolume() {
      this.$q.dialog({
        component: VolumeDialog,
        parent: this
      });
    }
  }
};
</script>
