<template>
  <q-input
    ref="otp"
    borderless
    outlined
    label="OTP"
    :rules="[validateOtp]"
    input-class="text-mono text-h6 otp-input"
    autogrow
    mask="######"
    fill-mask
    lazy-rules
    v-model="form"
  />
</template>

<script>
import QrCode from "qrcode.vue";
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  methods: {
    validateOtp(v) {
      if (!(v ?? "").match(/^\d{6}$/)) {
        return "Invalid format";
      }
    },
    validate() {
      return this.$refs.otp.validate();
    }
  }
};
</script>
<style>
.otp-input {
  font-size: 1.8em;
  --spacing: 0.3em;
  margin-left: 0.4em;
  width: calc(6ch + (var(--spacing) * 7));
  letter-spacing: var(--spacing);
}
</style>
