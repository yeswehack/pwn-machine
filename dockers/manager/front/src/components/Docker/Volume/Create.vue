<template>
  <q-form @submit="submit">
    <q-card-section class="q-gutter-md">
      <q-input v-model="form.name" required label="Name" />
      <q-list separator class="rounded-borders" bordered>
        <component
          :is="formChildren.labels"
          v-model="form.labels"
          icon="label"
          label="Labels"
          :caption="`${form.labels.length} label(s)`"
        />
      </q-list>
    </q-card-section>

    <q-card-section>
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </q-form>
</template>

<script>
import KeyValueListInput from "../KeyValueListInput.vue";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";
import api from "src/api";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    labels: KeyValueListInput
  },
  methods: {
    submit(done) {
      const name = this.form.name ?? "<unnamed>";
      this.mutate({
        mutation: api.docker.volumes.CREATE_VOLUME,
        variables: { input: this.form },
        refetchQueries: [{ query: api.docker.volumes.LIST_VOLUMES }],
        message: `Volume ${name} created.`
      })
        .then(() => {
          this.$emit("ok");
          this.$emit("created", this.form.name);
        })
        .finally(done);
    }
  }
};
</script>
