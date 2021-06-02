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
              label="Current password"
              type="password"
              v-model="currentPassword"
            />
          </q-card-section>
          <q-card-section>
            <q-input
              label="New password"
              type="password"
              v-model="newPassword"
            />
            <q-input
              label="Confirm password"
              type="password"
              v-model="repeatedPassword"
            />
          </q-card-section>
          <q-card-actions vertical>
            <q-btn
              color="positive"
              :disable="newPassword !== repeatedPassword"
              type="submit"
            >
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

export default {
  data: () => ({
    currentPassword: "",
    newPassword: "",
    repeatedPassword: ""
  }),
  methods: {
    async submit() {
      if (this.newPassword !== this.repeatedPassword) return;

      const {
        data: { updateAuthPassword }
      } = await this.$apollo.mutate({
        mutation: api.auth.UPDATE_PASSWORD,
        variables: {
          current: this.currentPassword,
          new: this.newPassword
        }
      });

      if (updateAuthPassword) {
        this.$router.push({ name: "login" });
      }
    }
  }
};
</script>
