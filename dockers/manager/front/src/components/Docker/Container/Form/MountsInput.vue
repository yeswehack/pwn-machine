<template>
  <q-expansion-item
    icon="eva-hard-drive-outline"
    label="Mounts"
    :caption="`${form.length} mount(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <base-grid-input
          :readonly="readonly"
          :titles="['Type', 'Name/Source', 'Target', 'Read Only']"
          grid-format="85px 1fr 1fr auto"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-select
              v-model="model.type"
              flat
              :options="['volume', 'bind', 'tmpfs']"
              label="Type"
              @keypress.enter.prevent="addEntry"
            />
            <div v-if="model.type === 'volume'" style="overflow: hidden">
              <q-select
                v-model="model.name"
                flat
                :options="volumeOptions"
                label="Name"
                @keypress.enter.prevent="addEntry"
              >
                <template #selected-item="{opt}">
                  <div class="ellipsis">{{ opt }}</div>
                </template>
              </q-select>
            </div>
            <div v-if="model.type === 'bind'" style="overflow: hidden">
              <q-input
                v-model="model.source"
                flat
                label="Source"
                @keypress.enter.prevent="addEntry"
              />
            </div>
            <div v-if="model.type === 'tmpfs'" style="overflow: hidden">
              <q-input disable value="-" flat />
            </div>
            <q-input
              v-model="model.target"
              class="col"
              flat
              label="Target"
              @keypress.enter.prevent="addEntry"
            />
            <div>
              <q-toggle v-model="model.readonly" checked-icon="lock" />
              <q-tooltip anchor="top middle" self="bottom middle">
                {{ model.readonly ? "Read only" : "Read/Write" }}
              </q-tooltip>
            </div>
          </template>
          <template #entry="{entry}">
            <div>
              {{ entry.type }}
            </div>
            <div v-if="entry.type === 'volume'" class="ellipsis">
              <volume-link :name="entry.name" />

              <q-popup-edit v-model="entry.name">
                <q-input
                  v-model="entry.name"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>

            <div v-if="entry.type === 'bind'" class="ellipsis">
              {{ entry.source }}

              <q-popup-edit v-model="entry.source">
                <q-input
                  v-model="entry.source"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div v-if="entry.type === 'tmpfs'" class="ellipsis">
              -
            </div>
            <div class="ellipsis">
              {{ entry.target }}

              <q-popup-edit v-model="entry.target">
                <q-input
                  v-model="entry.target"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div>
              <q-toggle
                v-model="entry.readonly"
                :disable="readonly"
                checked-icon="lock"
              />
              <q-tooltip anchor="top middle" self="bottom middle">
                {{ entry.readonly ? "Read only" : "Read/Write" }}
              </q-tooltip>
            </div>
          </template>
        </base-grid-input>
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
import BaseGridInput from "src/components/BaseGridInput.vue";
import VolumeDialog from "../../Volume/Dialog.vue";

const defaultModel = {
  type: "volume",
  name: null,
  source: null,
  target: null,
  readonly: false
};

export default {
  components: { VolumeLink, BaseGridInput },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: [],
  apollo: {
    dockerVolumes: {
      query: api.docker.volumes.LIST_VOLUMES
    }
  },
  data: () => ({ model: defaultModel }),
  computed: {
    volumeOptions() {
      return (this.dockerVolumes ?? []).map(v => v.name);
    },
    currentType() {
      return this.model.type;
    }
  },
  watch: {
    currentType() {
      this.model.name = null;
      this.model.source = null;
    }
  },
  methods: {
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = defaultModel;
    },
    createVolume() {
      this.$q.dialog({
        component: VolumeDialog,
        parent: this
      });
    }
  }
};
</script>
