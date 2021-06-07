<template>
  <q-input
    ref="otp"
    outlined
    label="OTP"
    input-class="text-mono text-h5 text-center otp-input q-my-sm"
    autogrow
    mask="######"
    fill-mask
    @keypress.enter="$emit('enter')"
    :rules="[isTotp]"
    v-model="form"
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  formDefinition: "",
  methods: {
    isTotp: v => +v || "Code must be 6 digits long",
    validate() {
      return this.$refs.otp.validate();
    }
  }
};
</script>

<style>
.otp-input {
  width: 10ch;
  text-indent: 0.5ch;
  letter-spacing: 0.5ch;
}
</style>
