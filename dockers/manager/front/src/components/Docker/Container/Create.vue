<template>
  <q-form @submit="submit">
    <q-card-section class="column q-gutter-md">
      <div class="col">
        <div class="column  q-gutter-sm">
          <q-input v-model="form.name" label="name" />
          <image-select v-model="form.image" />
        </div>
      </div>
      <q-list  separator class="rounded-borders" bordered>
        <component :is="formChildren.extra" v-model="form.extra" />
        <component :is="formChildren.environment" v-model="form.environment" />
        <component :is="formChildren.labels" v-model="form.labels" />
        <component :is="formChildren.volumes" v-model="form.volumes" />
      </q-list>
    </q-card-section>
    <q-card-actions align="right" class="q-pa-md q-gutter-md">
      <q-toggle
        color="negative"
        v-model="form.rm"
        label="Delete on stop"
        left-label
      />
      <q-toggle
        color="positive"
        v-model="form.start"
        label="Start the container"
        left-label
      />
      <q-btn color="positive" type="submit" class="q-py-xs q-px-md col-2">
        {{ form.start ? "Start" : "Create" }}
      </q-btn>
    </q-card-actions>
    <q-card-actions v-if="true">
      <pre>{{ JSON.stringify(form, null, 2) }}</pre>
    </q-card-actions>
  </q-form>
</template>

<script>
import ImageSelect from "./Form/ImageSelect.vue";
import ExtraConfig from "./Form/ExtraConfig.vue";
import VolumeSettings from "./Form/VolumeSettings.vue";
import DeepForm from "src/mixins/DeepForm.js";
import EnvironInput from "./Form/EnvironInput.vue";
import LabelInputVue from "../LabelInput.vue";
export default {
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    image: null,
    labels: LabelInputVue,
    environment: EnvironInput,
    extra: ExtraConfig,
    volumes: VolumeSettings
  },
  components: {
    ImageSelect,
    EnvironInput,
    ExtraConfig
  },
  methods: {
    submit() {
      this.$emit("submit", this.form);
    }
  }
};
</script>
