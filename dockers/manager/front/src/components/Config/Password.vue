<template>
  <div class="row justify-center full-width">
    <div class="col col-auto">
      <q-form @submit="submit">
        <q-card bordered style="width:500px">
          <q-card-section class="text-h6">
            Change password
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-input
              required
              label="Current password"
              type="password"
              v-model="form.old"
            />
          </q-card-section>
          <q-card-section>
            <component :is="formChildren.new" v-model="form.new" />
          </q-card-section>
          <q-card-actions vertical>
            <q-btn color="positive" type="submit">
              Submit
            </q-btn>
          </q-card-actions>
        </q-card>
      </q-form>
    </div>
  </div>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import PasswordInput from "./PasswordInput.vue";
import { notify } from 'src/utils';

export default {
  mixins: [DeepForm],
  formDefinition: {
    old: null,
    new: PasswordInput
  },
  data: () => ({}),
  methods: {
    async submit() {
      this.mutate({
        mutation: api.auth.UPDATE_PASSWORD,
        variables: this.form,
        message: "Password changed."
      })
    }
  }
};
</script>
