<template>
  <q-form @submit="submit">
    <q-card-section class="q-gutter-md">
      <q-input v-if="!readonly" v-model="form.name" autofocus label="Name" />
      <image-input v-if="!readonly" ref="image" v-model="image" />
      <q-list separator class="rounded-borders" bordered>
        <component
          :is="formChildren.extra"
          v-model="extra"
          :readonly="readonly"
        />
        <component
          :is="formChildren.environment"
          v-model="form.environment"
          :readonly="readonly"
          icon="attach_money"
          label="Environment"
          :caption="`${form.environment.length} variable(s)`"
        />
        <component
          :is="formChildren.labels"
          v-model="form.labels"
          :readonly="readonly"
          icon="label"
          label="Labels"
          :caption="`${form.labels.length} label(s)`"
        />
        <component
          :is="formChildren.ports"
          v-model="form.ports"
          :readonly="readonly"
        />
        <component
          :is="formChildren.network"
          v-if="!readonly"
          v-model="form.network"
        />
        <component
          :is="formChildren.mounts"
          v-model="form.mounts"
          :readonly="readonly"
        />
      </q-list>
    </q-card-section>
    <q-card-section v-if="!readonly" class="row q-gutter-md">
      <div class="col col-auto">
        <q-toggle
          v-model="form.start"
          color="positive"
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
import KeyValueListInput from "../KeyValueListInput.vue";
import NetworkInput from "./Form/NetworkInput.vue";
import ExposedPorts from "./Form/ExposedPorts.vue";
import ImageInput from "./Form/ImageInput.vue";
import api from "src/api";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  components: { ExtraConfig, ImageInput, ResetAndSave },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: {
    start: true,
    name: null,
    image: null,
    labels: KeyValueListInput,
    environment: KeyValueListInput,
    extra: ExtraConfig,
    ports: null,
    capAdd: null,
    capDrop: null,
    restartPolicy: null,
    user: null,
    command: null,
    mounts: MountsInput,
    network: NetworkInput,
    ports: ExposedPorts
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
    submit(done) {
      const input = Object.assign({}, this.form);
      delete input["extra"];
      this.mutate({
        mutation: api.docker.containers.CREATE_CONTAINER,
        variables: { input },
        refetchQueries: [{ query: api.docker.containers.LIST_CONTAINERS }],
        message: `Container created`
      }).finally(done);
    }
  }
};
</script>
