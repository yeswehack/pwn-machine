<template>
  <q-form @submit="submit">
    <q-card-section>
      <div class="row q-gutter-md items-center">
        <div class="col">
          <q-input
            ref="name"
            :readonly="readonly"
            :rules="[required('Name is required')]"
            v-model="form.name"
            required
            label="Name"
          />
        </div>
        <div class="col col-auto">
          <q-checkbox
            :disable="readonly"
            left-label
            label="Internal"
            v-model="form.internal"
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
        />
      </q-list>
    </q-card-section>

    <q-card-section v-if="!readonly">
      <reset-and-save
        :modified="modified"
        @save="submit"
        :validate="validate"
        @reset="reset"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import LabelInput from "../LabelInput.vue";
import IpamsInput from "./IpamsInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import api from "src/api";
import { notify } from "src/utils";
import { required } from "src/utils/validators";

export default {
  props: { readonly: { type: Boolean, default: false } },
  mixins: [DeepForm],
  components: { ResetAndSave, LabelInput },
  formDefinition: {
    internal: false,
    name: null,
    ipams: IpamsInput,
    labels: LabelInput
  },
  data() {
    return { required };
  },
  methods: {
    validate() {
      return this.$refs.name.validate();
    },
    async submit() {
      this.mutate({
        mutation: api.docker.networks.CREATE_NETWORK,
        variables: { input: this.form },
        refetchQueries: [{ query: api.docker.networks.LIST_NETWORKS }],
        message: `Network ${this.form.name} created.`
      }).then(r => {
        this.$emit("ok");
        this.$emit("created", this.form.name);
      });
    }
  }
};
</script>
