<template>
  <q-form @submit="submit">
    <q-card-section >
      <div class="row q-gutter-md items-center">
        <div class="col">
          <q-input :readonly="readonly" v-model="form.name" required label="Name" />
        </div>
        <div class="col col-auto">
          <q-checkbox :disable="readonly" left-label label="Internal" v-model="form.internal" />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-gutter-sm">
      <q-list separator class="rounded-borders" bordered>
        <component
          :is="formChildren.ipam"
          v-model="form.ipam"
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
import IpamInput from "./IpamInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  props: { readonly: { type: Boolean, default: false } },
  mixins: [DeepForm],
  components: { ResetAndSave, LabelInput },
  formDefinition: {
    internal: false,
    name: null,
    ipam: IpamInput,
    labels: LabelInput
  },
  methods: {
    async submit() {
      this.$emit("ok");
    }
  }
};
</script>
