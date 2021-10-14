<template>
  <base-grid-input
    :titles="['Tags']"
    grid-format="1fr"
    :entries="form"
    :loading="loading"
    @addEntry="addTag"
    @removeEntry="removeTag"
  >
    <template #inputs>
      <q-input v-model="model" label="New tag" />
    </template>
  </base-grid-input>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";
import api from "src/api";
export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  formDefinition: [],
  props: {
    imageId: { type: String, required: true }
  },
  data: () => ({ model: null, loading: false }),
  methods: {
    doRemoveTag(tag) {
      this.mutate({
        mutation: api.docker.images.DELETE_IMAGE,
        variables: { id: tag, force: false },
        refetchQueries: [{ query: api.docker.images.LIST_IMAGES }],
        message: `Tag ${tag} removed.`
      });
    },
    addTag() {
      if (!this.model) return;
      const [repository, tag] = this.model.split(":");
      this.loading = true;
      this.mutate({
        mutation: api.docker.images.TAG_IMAGE,
        variables: { id: this.imageId, repository, tag },
        refetchQueries: [{ query: api.docker.images.LIST_IMAGES }],
        message: `Tag ${this.model} added.`
      })
        .then(() => {
          this.model = null;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    removeTag(idx) {
      const tag = this.form[idx];
      if (this.form.length > 1) {
        this.doRemoveTag(tag);
        return;
      }
      this.$q
        .dialog({
          type: "confirm",
          title: "Are you sure ?",
          message: "Removing the last tag will delete the image.",
          cancel: true,
          ok: true
        })
        .onOk(() => {
          this.doRemoveTag(tag);
        });
    }
  }
};
</script>
