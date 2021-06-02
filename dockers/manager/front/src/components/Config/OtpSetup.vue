<template>
  <div>
    <q-card-section>
      <div class="q-gutter-sm">
        <p>Scan this image with your favorite TOTP app:</p>
        <div class="row justify-center q-my-md">
          <div class="col col-auto qr-container">
            <qr-code :value="totpUri" size="250" class="rounded-borders" />
          </div>
        </div>
        <p>or enter this code manually:</p>
        <span class="flex flex-center q-mt-sm text-mono">{{ totpSecret }}</span>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <p>
        Type the 6 digits displayed by the app:
      </p>
      <div class="row justify-center">
        <div class="col col-auto">
          <component ref="otp" :is="formChildren" v-model="form"/>
        </div>
      </div>
    </q-card-section>
  </div>
</template>

<script>
import QrCode from "qrcode.vue";
import api from "src/api";
import DeepForm from 'src/mixins/DeepForm';
import OtpInput from './OtpInput.vue';

export default {
  mixins: [DeepForm],
  formDefinition: OtpInput,
  components: { QrCode },
  apollo: {
    totpUri: {
      query: api.auth.GET_TOTP_URI,
      update: ({ authTotpUri }) => authTotpUri
    }
  },
  computed: {
    totpSecret() {
      if (!this.totpUri) return undefined;
      return new URL(this.totpUri).searchParams.get("secret");
    }
  },
  methods: {
    validate() {
      return this.$refs.otp.validate();
    },
  }
};
</script>

<style lang="scss" scoped>
.qr-container {
  div {
    box-sizing: content-box;
    height: 250px;
    border: 10px solid;
  }
}
</style>
