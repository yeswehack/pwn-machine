<template>
  <q-page padding>
    <div class="row justify-center">
      <q-form class="login-form" @submit="submit">
        <q-card>
          <q-card-section>
            <div class="text-h6">
              Authentication required
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-input
              type="password"
              label="Password"
              v-model="password"
              required
            />
            <q-input
              type="number"
              min="0"
              label="OTP"
              v-model.number="otp"
              required
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
            <q-btn color="green" type="submit">Login</q-btn>
          </q-card-actions>
        </q-card>
      </q-form>
    </div>
    <!-- content -->
  </q-page>
</template>

<script>
import { login as loginMutation } from "src/gql/auth/mutations";

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
  created() {
    this.expireOptions = expireOptions;
  },
  data: () => ({
    password: null,
    otp: null,
    expire: null
  }),
  methods: {
    async submit() {
      try {
        const {
          data: { login }
        } = await this.$apollo.mutate({
          mutation: loginMutation,
          variables: {
            password: this.password,
            otp: this.otp,
            expire: this.expire
          }
        });
        this.$store.commit("setToken", login);
        this.$router.push({ name: "index" });
      } catch ({ graphQLErrors }) {
        graphQLErrors.forEach(({ message }) => {
          this.$q.notify({
            color: "negative",
            message,
            position: "top",
            timeout: 3000
          });
        });
      }
    }
  }
};
</script>

<style lang="css" scoped>
.login-form {
  width: max(400px, 50%);
}
</style>
