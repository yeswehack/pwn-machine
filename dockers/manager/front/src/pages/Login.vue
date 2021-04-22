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
              v-model="otp"
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
];

export default {
  created() {
    this.expireOptions = expireOptions;
  },
  data: () => ({
    password: null,
    otp: null,
    expire: expireOptions[0].value,
  }),
  methods: {
    async submit() {
      const r =
        await fetch("/api/login", {
          method: "POST",
          body: new URLSearchParams({
            password: this.password,
            otp: this.otp,
            expire: this.expire,
          })
        });

      if (r.ok) {
        this.$router.push({name: "index"});
      } else {
        this.$q.notify({
          color: "negative",
          message: await r.text(),
          position: "top",
          timeout: 3000
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
