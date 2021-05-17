<template>
  <q-form @submit="submit">
    <q-card-section class="q-col-gutter-md">
      <q-input v-model="form.name" filled required label="Name" />
      <q-checkbox label="Internal" v-model="form.internal" />
    </q-card-section>
    <q-card-section class="q-gutter-sm">
      <q-expansion-item
        expand-separator
        icon="eva-share-outline"
        label="IPAM Settings"
        :caption="ipamCaption"
      >
        <component ref="ipam" :is="formChildren.ipam" v-model="form.ipam" />
      </q-expansion-item>
      <label-input v-model="form.labels" />
    </q-card-section>

    <q-card-section>
      <reset-and-save :modified="modified" @save="submit" @reset="reset" />
    </q-card-section>
  </q-form>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import api from "src/api";
import LabelInput from "../LabelInput.vue";
import IpamInput from "./IpamInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  mixins: [DeepForm],
  components: { ResetAndSave, LabelInput },
  formDefinition: {
    internal: false,
    name: null,
    ipam: IpamInput,
    labels: []
  },
  computed: {
    ipamCaption() {
      return this.form.ipam.subnet || this.form.ipam.gateway
        ? "custom"
        : "automatic";
    }
  },
  methods: {
    async submit() {
      this.$emit("ok");
    }
  }
};
</script>
