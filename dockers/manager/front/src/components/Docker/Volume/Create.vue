<template>
  <q-form @submit="submit">
    <q-card-section class="q-gutter-md">
      <q-input v-model="form.name" required label="Name" />
      <q-list separator class="rounded-borders" bordered>
        <component :is="formChildren.labels" v-model="form.labels" />
      </q-list>
    </q-card-section>

    <q-card-section>
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </q-form>
</template>

<script>
import LabelInput from "../LabelInput.vue";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    labels: LabelInput
  },
  methods: {
    async submit() {
    }
  }
};
</script>

