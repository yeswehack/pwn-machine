<template>
  <q-form @submit="submit">
    <q-card-section>
      <div class="row q-gutter-md items-end">
        <div class="col">
          <q-input
            :readonly="readonly"
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
        <div class="col col-auto">
          <q-checkbox
            :disable="readonly"
            left-label
            label="enable IPv6"
            v-model="form.ipv6"
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
      <reset-and-save :modified="modified" @save="submit" @reset="reset" />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import LabelInput from "../LabelInput.vue";
import IpamsInput from "./IpamsInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import api from "src/api";

export default {
  props: { readonly: { type: Boolean, default: false } },
  mixins: [DeepForm],
  components: { ResetAndSave, LabelInput },
  formDefinition: {
    internal: false,
    ipv6: false,
    name: null,
    ipams: IpamsInput,
    labels: LabelInput
  },
  methods: {
    async submit() {
      this.$apollo
        .mutate({
          mutation: api.docker.network.CREATE_NETWORK,
          variables: { input: this.form },
          refetchQueries: [{ query: api.docker.network.LIST_NETWORKS }]
        })
        .then(() => {
          this.$q.notify({
            message: `Network ${this.form.name} created.`,
            type: "positive"
          });
          this.$emit("ok");
          this.$emit("created", this.form.name);
        });
    }
  }
};
</script>
