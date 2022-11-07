<template>
  <q-form @submit="submit">
    <q-card-section>
      <div class="row q-gutter-md items-center">
        <div class="col">
          <q-input
            ref="name"
            v-model="form.name"
            :readonly="readonly"
            :rules="[required('Name is required')]"
            required
            autofocus
            label="Name"
          />
        </div>
        <div class="col col-auto">
          <q-checkbox
            v-model="form.internal"
            :disable="readonly"
            left-label
            label="Internal"
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-gutter-sm">
      <q-list separator class="rounded-borders" bordered>
        <component
          :is="formChildren.ipams"
          v-model="form.ipams"
          :readonly="readonly"
        />
        <component
          :is="formChildren.labels"
          v-model="form.labels"
          :readonly="readonly"
          icon="label"
          label="Labels"
          :caption="`${form.labels.length} label(s)`"
        />
      </q-list>
    </q-card-section>

    <q-card-section v-if="!readonly">
      <reset-and-save
        :modified="modified"
        :validate="validate"
        @save="submit"
        @reset="reset"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import KeyValueListInput from "../KeyValueListInput.vue";
import IpamsInput from "./IpamsInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import api from "src/api";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: {
    internal: false,
    name: null,
    ipams: IpamsInput,
    labels: KeyValueListInput
  },
  methods: {
    validate() {
      return this.$refs.name.validate();
    },
    submit(done) {
      this.mutate({
        mutation: api.docker.networks.CREATE_NETWORK,
        variables: { input: this.form },
        refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }],
        message: `Network ${this.form.name} created.`
      })
        .then(() => {
          this.$emit("ok", this.form.name);
        })
        .finally(done);
    }
  }
};
</script>
