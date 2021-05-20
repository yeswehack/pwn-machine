<template>
  <base-details :errors="value.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section class="text-h6">
            {{ value.name }}
          </q-card-section>

          <q-card-section>
            <component
              :is="formChildren.extra"
              v-model="form.extra"
              hide-title
            />
          </q-card-section>
          <q-card-section>
            <reset-and-save
              :modified="modified"
              @save="submit"
              @reset="reset"
            />
          </q-card-section>
        </q-card>
      </div>
    </template>
  </base-details>
</template>

<script>
import { getCreateComponent } from "./Create.vue";
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";
import api from "src/api";
export default {
  components: { CreateMiddleware, BaseDetails, ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    extra(value) {
      return getCreateComponent(value);
    }
  },
  methods: {
    submit(done) {
      console.log(this.value);
      const mutation = api.traefik.UPDATE_MIDDLEWARE[this.value.type];
      this.$apollo
        .mutate({
          mutation,
          variables: { nodeId: this.value.nodeId, patch: this.form.extra },
          refetchQueries: [{ query: api.traefik.GET_MIDDLEWARES }]
        })
        .then(done);
    }
  }
};
</script>
