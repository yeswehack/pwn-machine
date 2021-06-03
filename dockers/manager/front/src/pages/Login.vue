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
                type="password"
                label="Password"
                v-model="form.password"
              />
              <div class="row ">
                <div class="col col-auto">
                  <component :is="formChildren.otp" v-model="form.otp" />
                </div>
              </div>
              <q-select
                label="Remember me"
                :options="expireOptions"
                emit-value
                map-options
                v-model="form.expire"
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
import _ from "lodash";
import api from "src/api";
import { notify } from "src/utils";
import DeepForm from "src/mixins/DeepForm";
import OtpInput from "src/components/Config/OtpInput.vue";

const dayDuration = 60 * 60 * 24;

export default {
  mixins: [DeepForm],
  formDefinition: {
    password: null,
    otp: OtpInput,
    expire: dayDuration
  },
  data: () => {
    const expireOptions = [
      {
        label: "One day",
        value: dayDuration
      },
      {
        label: "One week",
        value: dayDuration * 7
      },
      {
        label: "One month",
        value: dayDuration * 30
      },
      {
        label: "Forever",
        value: null
      }
    ];
    return {
      expireOptions
    };
  },
  methods: {
    submit() {
      this.mutate({
        mutation: api.auth.LOGIN,
        variables: this.form,
        message: "Logged in."
      }).then(result => {
        localStorage.setItem("token", result.token);
        this.$router.push({ name: "index" });
      });
    }
  }
};
</script>
