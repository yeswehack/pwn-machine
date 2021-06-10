<template>
  <div class="row justify-evenly full-width q-gutter-md">
    <div class="col col-auto">
      <q-form @submit="changePassword">
        <q-card bordered style="width:500px">
          <q-card-section class="text-h6">
            Change admin password
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-input
              v-model="oldPassword"
              label="Current password"
              type="password"
              :rules="[required('Please enter your current password')]"
            />
          </q-card-section>
          <q-separator class="q-mx-xl" />
          <q-card-section>
            <password-input v-model="newPassword" />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              label="Change"
              color="positive"
              icon="eva-save"
              type="submit"
            />
          </q-card-actions>
        </q-card>
      </q-form>
    </div>
    <div class="col col-auto">
      <q-form @submit="resetToken">
        <q-card bordered style="width:500px">
          <q-card-section class="text-h6">
            Invalidate all tokens
          </q-card-section>
          <q-separator />
          <q-card-section>
            <p>
              This will generate a new secret for Pwn-Machine, by doing so all
              active JWT will become invalid. <br />
              You will be logged-out.
            </p>
          </q-card-section>
          <q-card-section>
            <q-toggle
              v-model="confirmReset"
              label="Are you sure you want to continue ?"
            />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn
              :disable="!confirmReset"
              label="Reset"
              color="positive"
              icon="eva-loader-outline"
              type="submit"
            />
          </q-card-actions>
        </q-card>
      </q-form>
    </div>
  </div>
</template>

<script>
import api from "src/api";
import PasswordInput from "./PasswordInput.vue";
import { required } from "src/mixins/DeepForm.js";
export default {
  components: { PasswordInput },
  data: () => ({ confirmReset: false, newPassword: null, oldPassword: null, required }),
  methods: {
    async changePassword() {
      this.mutate({
        mutation: api.auth.UPDATE_PASSWORD,
        variables: { old: this.oldPassword, new: this.newPassword },
        message: "Password changed."
      });
    },
    async resetToken() {
      this.mutate({
        mutation: api.auth.RESET_JWT_SECRET,
        message: "JWT secret reseted."
      });
    }
  }
};
</script>
