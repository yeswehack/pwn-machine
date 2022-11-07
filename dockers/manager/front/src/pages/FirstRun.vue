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
            <q-stepper ref="stepper" v-model="step" animated>
              <q-step
                name="password"
                title="Create admin password"
                icon="eva-lock"
              >
                <component
                  :is="formChildren.password"
                  ref="password"
                  v-model="form.password"
                />
              </q-step>
              <q-step name="otp" title="Initialize OTP" icon="eva-keypad">
                <component
                  :is="formChildren.otp"
                  ref="otp"
                  v-model="form.otp"
                  @keyup.enter="submit"
                />
              </q-step>

              <template #navigation>
                <q-card-section>
                  <reset-and-save
                    :step.sync="step"
                    :steps="steps"
                    :modified="modified"
                    @reset="reset"
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
import PasswordInput from "src/components/Auth/PasswordInput.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import DeepForm from "src/mixins/DeepForm";
import OtpSetup from "src/components/Auth/OtpSetup.vue";
import api from "src/api";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    password: PasswordInput,
    otp: OtpSetup
  },
  data() {
    const steps = [
      {
        name: "password",
        validate: () => this.$refs.password.validate()
      },
      {
        name: "otp",
        validate: () => this.$refs.otp.validate()
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
          localStorage.setItem("token", result);
          this.$router.push({ name: "index" });
        })
        .finally(done);
    }
  }
};
</script>
