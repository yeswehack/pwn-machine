<template>
  <div>
    <q-card-section class="q-gutter-md">
      <q-input v-model="form.tag" label="Tag" />
      <q-input
        v-model="form.url"
        filled
        label="Url"
        hint="Can be a link to a tar archive or a git repository"
      />
    </q-card-section>
    <q-card-section class="q-mt-md">
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </div>
</template>

<script>
import ResetAndSave from 'src/components/ResetAndSave.vue'
import DeepForm from 'src/mixins/DeepForm'
import { GlobalBus } from 'src/eventBus';
export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    url: null,
    tag: null,
  },
  methods: {
    submit (done) {
      const { url, tag } = this.form

      GlobalBus.$emit("buildDockerImage", {
        url, tag, done: () => {
          done()
          this.$emit("done")
        }
      })
      this.$emit("ok", tag.includes(":") ? tag : `${tag}:latest`)
    }
  }

}
</script>

<style>
</style>