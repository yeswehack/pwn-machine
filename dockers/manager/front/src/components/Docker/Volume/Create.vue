<template>
  <q-card bordered class="create-volume">
    <q-form @submit="submit">
      <q-card-section>
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new volume</div>
          <q-space />
          <a
            class="text-white"
            href="https://docs.docker.com/engine/reference/commandline/volume_create/"
            target="_blank"
          >
            <q-icon size="sm" name="help" />
          </a>
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-col-gutter-md">
        <q-input v-model="form.name" required label="Name" />
        <KeyValueTable title="Labels" v-model="form.labels" />
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md">
          Create
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import KeyValueTable from "src/components/KeyValueTable.vue";

export default {
  components: { KeyValueTable },
  props: {
    info: {
      type: Object,
      default: null
    }
  },
  data() {
    const form = { name: "", labels: {} };
    if (this.info) {
      form.name = this.info.Name;
      Object.assign(form.labels, this.info.Labels);
    }
    return { form };
  },
  methods: {
    async submit() {
      const volume = {
        Name: this.form.name,
        Labels: this.form.labels
      };

      const response = await this.$api.docker.createVolume(volume);

      if ("error" in response) {
        this.$q.notify({
          color: "negative",
          message: response.error
        });
      } else {
        this.$q.notify({
          color: "positive",
          message: `Volume ${this.form.name} created.`
        });
        this.$emit("created", response.name);
      }
    }
  }
};
</script>

<style>
.create-volume {
  min-width: 700px;
  max-width: 80vw;
}
</style>
