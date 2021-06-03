<template>
  <q-page padding>
    <div class="row justify-center">
      <div class="col col-auto">
        <q-card style="width: 600px">
          <q-card-section>
            <div class="text-h6 q-mb-md">Welcome to pwn machine</div>
            <div>
              We are almost ready, you just need to setup the authentication.
            </div>
          </q-card-section>
          <q-card-section>
            <q-stepper v-model="step" ref="stepper" animated>
              <q-step
                name="password"
                title="Create admin password"
                icon="eva-lock"
              >
                <component
                  ref="password"
                  :is="formChildren.password"
                  v-model="form.password"
                />
              </q-step>

              <q-step name="otp" title="Initialize OTP" icon="eva-keypad">
                <component
                  ref="otp"
                  :is="formChildren.otp"
                  v-model="form.otp"
                />
              </q-step>
              <template #navigation>
                <q-card-section>
                  <reset-and-save
                    @reset="reset"
                    :step.sync="step"
                    :steps="steps"
                    :modified="modified"
                    @save="submit"
                  />
                </q-card-section>
              </template>
            </q-stepper>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import PasswordInput from "src/components/Config/PasswordInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import DeepForm from "src/mixins/DeepForm";
import OtpSetup from "src/components/Config/OtpSetup.vue";
import api from "src/api";
import { notify } from "src/utils";
export default {
  mixins: [DeepForm],
  formDefinition: {
    password: PasswordInput,
    otp: OtpSetup
  },
  components: { ResetAndSave },
  data() {
    const steps = [
      {
        name: "password",
        validate: () => {
          return this.$refs.password.validate();
        }
      },
      {
        name: "otp",
        validate: () => {
          return this.$refs.otp.validate();
        }
      }
    ];
    return { step: "password", steps };
  },
  methods: {
    submit(done) {
      this.mutate({
        mutation: api.auth.INITIALIZE_AUTH,
        variables: this.form,
        message: "Setup complete!"
      })
        .then(result => {
          localStorage.setItem("token", result.token);
          this.$router.push({ name: "index" });
        })
        .finally(done);
    }
  }
};
</script>

<style></style>
