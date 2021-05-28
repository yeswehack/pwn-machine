<template>
  <q-form @submit="submit">
    <q-card-section class="column q-gutter-md">
      <div class="col" v-if="!readonly">
        <div class="column  q-gutter-sm">
          <q-input v-model="form.name" label="name" />
          <image-select v-model="form.image"  />
        </div>
      </div>
      <q-list separator class="rounded-borders" bordered>
        <component :readonly="readonly" :is="formChildren.extra" v-model="form.extra" />
        <component :readonly="readonly" :is="formChildren.environment" v-model="form.environment" />
        <component :readonly="readonly" :is="formChildren.labels" v-model="form.labels" />
        <component :readonly="readonly" :is="formChildren.ports" v-model="form.ports" />
        <component :readonly="readonly" :is="formChildren.mounts" v-model="form.mounts" />
      </q-list>
    </q-card-section>
    <q-card-actions align="right" class="q-pa-md q-gutter-md" v-if="!readonly">
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
import ExtraConfig from "./Form/ExtraConfig.vue";
import MountsInput from "./Form/MountsInput.vue";
import DeepForm from "src/mixins/DeepForm.js";
import EnvironInput from "./Form/EnvironInput.vue";
import LabelInputVue from "../LabelInput.vue";
import ExposedPorts from './Form/ExposedPorts.vue';
export default {
  props: {
    readonly: { type: Boolean, default: false }
  },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    image: null,
    labels: LabelInputVue,
    environment: EnvironInput,
    extra: ExtraConfig,
    mounts: MountsInput,
    ports: ExposedPorts
  },
  components: {
  },
  methods: {
    submit() {
      this.$emit("submit", this.form);
    }
  }
};
</script>
