<template>
  <div class="row justify-center full-width">
    <div class="col col-auto">
      <q-card bordered style="width:500px">
        <q-card-section class="text-h6">
          Set up 2-factor authentication
        </q-card-section>
        <q-separator />
        <q-card-section>
          Scan this image with your favorite authenticator app:
          <div id="qr-container" class="flex flex-center q-my-lg">
            <qr-code :value="totpUri" size="250" class="rounded-borders" />
          </div>
          or enter this code manually:
          <span class="flex flex-center q-mt-sm text-mono">{{
            totpSecret
          }}</span>
        </q-card-section>
        <q-separator />
        <q-card-section>
          Type the 6 digits displayed by the app:
          <q-form class="flex flex-center q-mt-sm" @submit="submit">
            <q-input
              borderless
              input-class="text-mono text-h6"
              input-style="width:8ch"
              mask="######"
              fill-mask
              v-model="totp"
            >
              <template v-slot:after>
                <q-btn color="positive" :disable="!+totp" @click="submit">
                  Submit
                </q-btn>
              </template>
            </q-input>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import QrCode from "qrcode.vue";
import api from "src/api";

export default {
  components: { QrCode },
  apollo: {
    totpUri: {
      query: api.auth.GET_TOTP_URI,
      update: ({ authTotpUri }) => authTotpUri
    }
  },
  data: () => ({ totp: "" }),
  computed: {
    totpSecret() {
      if (!this.totpUri) return undefined;
      return new URL(this.totpUri).searchParams.get("secret");
    }
  },
  methods: {
    async submit() {
      if (!+this.totp) return;

      const {
        data: { updateAuthTotp }
      } = await this.$apollo.mutate({
        mutation: api.auth.UPDATE_TOTP,
        variables: { uri: this.totpUri, totp: +this.totp }
      });

      if (updateAuthTotp) {
        this.$router.push({ name: "login" });
      } else {
        this.$q.notify({
          message: "Invalid code",
          color: "negative",
          position: "top"
        });
      }
    }
  }
};
</script>

<style lang="scss">
#qr-container > * {
  border: 10px solid;
}
</style>
