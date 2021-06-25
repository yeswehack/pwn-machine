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
              class="fit"
              flat
              :options="['volume', 'bind', 'tmpfs']"
              label="Type"
              @keypress.enter.prevent="addEntry"
            />
            <div class="fit overflow-hidden">
              <q-select
                v-if="model.type === 'volume'"
                ref="source"
                v-model="model.name"
                :rules="[required('Please select a volume')]"
                lazy-rules="ondemand"
                flat
                :options="volumeOptions"
                label="Name"
                @input="$refs.source.resetValidation()"
                @keypress.enter.prevent="addEntry"
              >
                <template #selected-item="{opt}">
                  <div class="ellipsis">{{ opt }}</div>
                </template>
              </q-select>
              <q-input
                v-else-if="model.type === 'bind'"
                ref="source"
                v-model="model.source"
                :rules="[required('A bind mount must have a source')]"
                lazy-rules="ondemand"
                flat
                label="Source"
                @input="$refs.source.resetValidation()"
                @keypress.enter.prevent="addEntry"
              />
              <q-input v-else ref="source" disable value="-" flat />
            </div>
            <q-input
              ref="target"
              v-model="model.target"
              :rules="[required('You must specify a mountpoint')]"
              lazy-rules="ondemand"
              class="col"
              flat
              label="Target"
              @input="$refs.target.resetValidation()"
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

              <q-popup-edit
                v-model="entry.name"
                :validate="required('Please select a volume')"
              >
                <template #default="{validate}">
                  <q-select
                    v-model="entry.name"
                    :rules="[validate]"
                    :options="volumeOptions"
                    :readonly="readonly"
                    dense
                    autofocus
                  />
                </template>
              </q-popup-edit>
            </div>

            <div v-if="entry.type === 'bind'" class="ellipsis">
              {{ entry.source }}

              <q-popup-edit
                v-model="entry.source"
                :validate="required('A bind mount must have a source')"
              >
                <template #default="{validate}">
                  <q-input
                    v-model="entry.source"
                    :rules="[validate]"
                    :readonly="readonly"
                    dense
                    autofocus
                  />
                </template>
              </q-popup-edit>
            </div>
            <div v-if="entry.type === 'tmpfs'" class="ellipsis">
              -
            </div>
            <div class="ellipsis">
              {{ entry.target }}

              <q-popup-edit
                v-model="entry.target"
                :validate="required('You must specify a mountpoint')"
              >
                <template #default="{validate}">
                  <q-input
                    v-model="entry.target"
                    :rules="[validate]"
                    :readonly="readonly"
                    dense
                    autofocus
                  />
                </template>
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
  data: () => ({ model: { ...defaultModel } }),
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
    addEntry() {
      if (!this.model.type) return;
      const fields = [this.$refs.source, this.$refs.target];
      if (fields.map(f => f.validate()).every(x => x)) {
        this.form.unshift(this.model);
        this.model = { ...defaultModel };
        fields.forEach(f => f.resetValidation());
      }
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
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
