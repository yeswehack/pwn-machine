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
          gridFormat="85px 1fr 1fr auto"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-select
              flat
              :options="['volume', 'bind', 'tmpfs']"
              v-model="model.type"
              @keypress.enter.prevent="addEntry"
              label="Type"
            />
            <div style="overflow: hidden" v-if="model.type == 'volume'">
              <q-select
                flat
                :options="volumeOptions"
                v-model="model.name"
                @keypress.enter.prevent="addEntry"
                label="Name"
              >
                <template #selected-item="{opt}">
                  <div class="ellipsis">{{ opt }}</div>
                </template>
              </q-select>
            </div>
            <div style="overflow: hidden" v-if="model.type == 'bind'">
              <q-input
                flat
                v-model="model.source"
                @keypress.enter.prevent="addEntry"
                label="Source"
              />
            </div>
            <div style="overflow: hidden" v-if="model.type == 'tmpfs'">
              <q-input disable value="-" flat />
            </div>
            <q-input
              class="col"
              flat
              v-model="model.target"
              @keypress.enter.prevent="addEntry"
              label="Target"
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
            <div class="ellipsis" v-if="entry.type == 'volume'">
              <volume-link :name="entry.name" />

              <q-popup-edit v-model="entry.name">
                <q-input
                  :readonly="readonly"
                  v-model="entry.name"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>

            <div class="ellipsis" v-if="entry.type == 'bind'">
              {{ entry.source }}

              <q-popup-edit v-model="entry.source">
                <q-input
                  :readonly="readonly"
                  v-model="entry.source"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis" v-if="entry.type == 'tmpfs'">
              -
            </div>
            <div class="ellipsis">
              {{ entry.target }}

              <q-popup-edit v-model="entry.target">
                <q-input
                  :readonly="readonly"
                  v-model="entry.target"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div>
              <q-toggle
                :disable="readonly"
                v-model="entry.readonly"
                checked-icon="lock"
              />
              <q-tooltip anchor="top middle" self="bottom middle">
                {{ entry.readonly ? "Read only" : "Read/Write" }}
              </q-tooltip>
            </div>
          </template>
        </base-grid-input>
      </q-card-section>
      <q-card-section v-if='!readonly'>
        <div class="row justify-end">
          <q-btn
            dense
            color="positive"
            icon="eva-plus"
            label="Create a new volume"
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
export default {
  props: {
    readonly: { type: Boolean, default: false }
  },
  mixins: [DeepForm],
  formDefinition: [
    { type: "volume", name: "pm_elasticsearch-data", target: "/data" },
    { type: "volume", name: "pm_elasticsearch-data2", target: "/data2" }
  ],
  components: { VolumeLink, BaseGridInput },
  apollo: {
    dockerVolumes: {
      query: api.docker.volumes.LIST_VOLUMES
    }
  },
  computed: {
    volumeOptions() {
      return (this.dockerVolumes ?? []).map(v => v.name);
    },
    currentType() {
      return this.model.type;
    }
  },
  data() {
    const model = this.getDefaultModel();
    return {
      model
    };
  },
  methods: {
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    getDefaultModel() {
      return {
        type: "volume",
        name: null,
        source: null,
        target: null,
        readonly: false
      };
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = this.getDefaultModel();
    }
  },
  watch: {
    currentType() {
      this.model.name = null;
      this.model.source = null;
    }
  }
};
</script>
