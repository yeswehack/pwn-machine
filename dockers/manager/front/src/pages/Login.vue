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
            <q-input type="password" label="Password" v-model="password" />
            <q-input type="number" label="OTP" v-model="otp" />
            <q-select
              :options="expireOptions"
              v-model="expire"
              label="Remember me"
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
export default {
  data() {
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
    return { password: null, otp: null, expire: null, expireOptions };
  },
  methods: {
    async submit() {
      const info = {
        password: this.password,
        otp: this.otp,
        expire: this.expire
      };
      const r = await this.$store.dispatch("authenticate", info);
      if (r === false) {
        this.$q.notify({
          color: "negative",
          message: "Invalid credentials",
          position: "top",
          timeout: 3000
        });
      } else {
        this.$router.push({name: "index"})
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
