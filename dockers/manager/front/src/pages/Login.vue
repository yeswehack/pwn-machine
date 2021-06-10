<template>
  <q-page padding>
    <div class="row justify-center q-pa-lg">
      <div class="col col-auto">
        <q-form @submit="submit">
          <q-card bordered style="width:500px">
            <q-card-section class="text-h6">
              Authentication required
            </q-card-section>
            <q-separator />
            <q-card-section class="q-gutter-md">
              <q-input
                v-model="form.password"
                type="password"
                label="Password"
                :rules="[required('Please enter your password')]"
              />
              <div class="row justify-center">
                <div class="col col-auto">
                  <component :is="formChildren.otp" v-model="form.otp" @enter="submit" />
                </div>
              </div>
              <q-select
                v-model="form.durationDays"
                label="Remember me"
                :options="expireOptions"
                emit-value
                map-options
              />
            </q-card-section>
            <q-card-actions vertical>
              <q-btn color="positive" type="submit">
                Login
              </q-btn>
            </q-card-actions>
          </q-card>
        </q-form>
      </div>
    </div>
  </q-page>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import OtpInput from "src/components/Auth/OtpInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: {
    password: "",
    otp: OtpInput,
    durationDays: 1
  },
  data: () => {
    const expireOptions = [
      {
        label: "One day",
        value: 1
      },
      {
        label: "One week",
        value: 7
      },
      {
        label: "One month",
        value: 30
      },
      {
        label: "Forever",
        value: 0
      }
    ];
    return { expireOptions };
  },
  methods: {
    submit() {
      this.mutate({
        mutation: api.auth.LOGIN,
        variables: { input: this.form },
        message: "Logged in."
      }).then(result => {
        localStorage.setItem("token", result);
        this.$router.push({ name: "index" });
      });
    }
  }
};
</script>
