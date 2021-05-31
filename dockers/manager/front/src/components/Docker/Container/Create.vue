<template>
  <q-form @submit="submit">
    <q-card-section class="q-gutter-md">
      <q-input v-model="form.name" label="name" v-if="!readonly" />
      <image-input ref="image" v-model="image" v-if="!readonly" />
      <q-list separator class="rounded-borders" bordered>
        <component
          :readonly="readonly"
          :is="formChildren.extra"
          v-model="extra"
        />
        <component
          :readonly="readonly"
          :is="formChildren.environment"
          v-model="form.environment"
        />
        <component
          :readonly="readonly"
          :is="formChildren.labels"
          v-model="form.labels"
        />
        <component
          :readonly="readonly"
          :is="formChildren.ports"
          v-model="form.ports"
        />
        <component
          :readonly="readonly"
          :is="formChildren.mounts"
          v-model="form.mounts"
        />
      </q-list>
    </q-card-section>
    <q-card-section class="row q-gutter-md" v-if="!readonly">
      <div class="col col-auto">
        <q-toggle
          color="positive"
          v-model="form.start"
          label="Start the container"
        />
      </div>
    </q-card-section>
    <q-card-section>
      <reset-and-save
        :modified="modified"
        :validate="validate"
        @save="submit"
        @reset="reset"
      />
    </q-card-section>
    <q-card-actions v-if="false">
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
import ExposedPorts from "./Form/ExposedPorts.vue";
import ImageInput from "./Form/ImageInput.vue";
import api from "src/api";
import ResetAndSave from "src/components/ResetAndSave.vue";
export default {
  props: {
    readonly: { type: Boolean, default: false }
  },
  mixins: [DeepForm],
  formDefinition: {
    start: true,
    name: null,
    image: null,
    labels: LabelInputVue,
    environment: EnvironInput,
    extra: ExtraConfig,
    ports: null,
    capAdd: null,
    capDrop: null,
    restartPolicy: null,
    user: null,
    command: null,
    mounts: MountsInput,
    ports: ExposedPorts
  },
  components: {
    EnvironInput,
    ExtraConfig,
    ImageInput,
    ResetAndSave
  },
  computed: {
    image: {
      get() {
        return this.value?.image?.name ?? null;
      },
      set(v) {
        this.form.image = v;
      }
    },
    extra: {
      get() {
        return {
          command: this.form.command,
          user: this.form.user,
          restartPolicy: this.form.restartPolicy,
          capAdd: this.form.capAdd,
          capDrop: this.form.capDrop
        };
      },
      set(v) {
        this.form = Object.assign({}, this.form, v);
      }
    }
  },
  methods: {
    validate() {
      return this.$refs.image.validate();
    },
    submit() {
      const input = Object.assign({}, this.form);
      delete input["extra"];
      this.$apollo
        .mutate({
          mutation: api.docker.containers.CREATE_CONTAINER,
          variables: { input },
          refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }]
        })
        .then(r => {
          this.$emit("ok", r);
        });
    }
  }
};
</script>
