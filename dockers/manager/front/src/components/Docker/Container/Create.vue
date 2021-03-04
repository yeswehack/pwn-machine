<template>
  <q-card bordered style="width: 700px; max-width: 80vw;">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new container</div>
          <q-space />
          <a
            class="text-white"
            href="https://docs.docker.com/engine/reference/commandline/container_create/"
            target="_blank"
          >
            <q-icon size="sm" name="help" />
          </a>
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <div>
          <q-input filled v-model="formData.name" label="name" />
        </div>
        <div>
          <ImageSelect v-model="formData.image" />
        </div>
        <div>
          <q-expansion-item
            expand-separator
            icon="settings"
            label="Extra config"
          >
            <div class="q-py-md">
              <ExtraConfig v-model="formData.extra" />
            </div>
          </q-expansion-item>
          <q-expansion-item
            expand-separator
            icon="reorder"
            label="Environment"
            :caption="`${Object.keys(formData.env).length} variable(s)`"
          >
            <div class="q-py-md">
              <KeyValueTable
                hidetitle
                class="bg-grey-9"
                v-model="formData.env"
              />
            </div>
          </q-expansion-item>
          <q-expansion-item
            expand-separator
            :caption="`${Object.keys(formData.labels).length} label(s)`"
            icon="label"
            label="Labels"
          >
            <div class="q-py-md">
              <KeyValueTable
                hidetitle
                v-model="formData.labels"
                class="bg-grey-9"
              />
            </div>
          </q-expansion-item>
          <q-expansion-item
            expand-separator
            icon="device_hub"
            label="Network settings"
            :caption="
              `${formData.network.networks.length} netwok(s), ${formData.network.ports.length} exposed port(s)`
            "
          >
            <div class="q-py-md">
              <NetworkSettings v-model="formData.network" />
            </div>
          </q-expansion-item>
          <q-expansion-item
            expand-separator
            icon="storage"
            label="Volumes"
            :caption="`${Object.keys(formData.volumes).length} volume(s)`"
          >
            <div class="q-py-md">
              <VolumeSettings v-model="formData.volumes" class="bg-grey-9" />
            </div>
          </q-expansion-item>
        </div>
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md q-gutter-md">
        <q-toggle
          color="negative"
          v-model="formData.rm"
          label="Delete on stop"
          left-label
        />
        <q-toggle
          color="positive"
          v-model="formData.start"
          label="Start the container"
          left-label
        />
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
          {{ formData.start ? "Start" : "Create" }}
        </q-btn>
      </q-card-actions>
      <q-card-actions v-if="true">
        <pre hidden>{{ JSON.stringify(formData, null, 2) }}</pre>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import ImageSelect from "./Form/ImageSelect.vue";
import KeyValueTable from "src/components/KeyValueTable.vue";
import ExtraConfig from "./Form/ExtraConfig.vue";
import NetworkSettings from "./Form/NetworkSettings.vue";
import VolumeSettings from "./Form/VolumeSettings.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: {
    ImageSelect,
    KeyValueTable,
    NetworkSettings,
    ExtraConfig,
    VolumeSettings
  },
  methods: {
    submit() {
      this.$emit("submit", this.formData);
    }
  }
};
</script>
