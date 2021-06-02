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
            <q-card-section>
              <q-input type="password" label="Password" v-model="password" />
              <q-input
                borderless
                label="Authenticator app code"
                input-class="text-mono text-h6"
                mask="######"
                fill-mask
                v-model="totp"
              />
              <q-select
                label="Remember me"
                :options="expireOptions"
                emit-value
                map-options
                v-model="expire"
              />
            </q-card-section>
            <q-card-actions vertical>
              <q-btn color="positive" :disable="!+totp" type="submit">
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

const dayDuration = 60 * 60 * 24;
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

export default {
  apollo: {
    setupNeeded: {
      query: api.auth.GET_SETUP_NEEDED,
      fetchPolicy: "no-cache",
      update: ({ authSetupNeeded }) => authSetupNeeded,
      result() {
        if (this.setupNeeded) {
          this.$router.push({
            name: "config" + _.capitalize(this.setupNeeded)
          });
        }
      }
    }
  },
  created() {
    this.expireOptions = expireOptions;
  },
  data: () => ({
    password: "",
    totp: "",
    expire: null
  }),
  methods: {
    async submit() {
      const {
        data: { createAuthToken }
      } = await this.$apollo.mutate({
        mutation: api.auth.CREATE_TOKEN,
        variables: {
          password: this.password,
          totp: +this.totp,
          expire: this.expire
        }
      });

      if (createAuthToken) {
        const { token, expire } = createAuthToken;
        localStorage.setItem("token", token);
        this.$router.push("/");
      } else {
        this.$q.notify({
          message: "Invalid credentials",
          color: "negative",
          position: "top"
        });
      }
    }
  }
};
</script>
