<template>
  <div>
    <q-card-section>
      <div class="q-gutter-sm">
        <p>Scan this image with your favorite TOTP app:</p>
        <div class="row justify-center q-my-md">
          <div class="col col-auto qr-container">
            <qr-code :value="otpUrl" size="250" class="rounded-borders" />
          </div>
        </div>
        <p>or enter this code manually:</p>
        <span class="flex flex-center q-mt-sm text-mono">{{ otpSecret }}</span>
      </div>
    </q-card-section>
    <q-separator />
    <q-card-section>
      <p>Type the 6 digits displayed by the app:</p>
      <div class="row justify-center">
        <div class="col col-auto">
          <component :is="formChildren" v-model="form" @enter="$emit('enter')" />
        </div>
      </div>
    </q-card-section>
  </div>
</template>

<script>
import QrCode from "qrcode.vue";
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import OtpInput from "./OtpInput.vue";

export default {
  components: { QrCode },
  mixins: [DeepForm],
  formDefinition: OtpInput,
  apollo: {
    otpSecret: {
      query: api.auth.GET_OTP_SECRET,
    }
  },
  computed:{
    otpUrl(){
      return `otpauth://totp/Pwn-Machine:admin?secret=${this.otpSecret}&issuer=Pwn-Machine`
    }
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
