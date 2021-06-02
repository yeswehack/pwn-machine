<template>
  <div>
    <q-input
      label="New password"
      type="password"
      ref="new"
      :rules="[required('Please enter a password')]"
      v-model="newPassword"
    />
    <q-input
      ref="confirm"
      label="Confirm password"
      type="password"
      lazy-rules=""
      :rules="[mustMatch]"
      v-model="form"
    />
  </div>
</template>

<script>
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import { mapGetter } from "src/mixins/DeepForm";
import { required } from "src/utils/validators.js";

export default {
  mixins: [DeepForm],
  formDefinition: null,
  data: () => ({
    required,
    currentPassword: "",
    newPassword: "",
  }),
  methods: {
    mustMatch(v) {
      if (v != this.newPassword) {
        return "Password doesn't match";
      }
    },
    validate() {
      return [this.$refs.new.validate(), this.$refs.confirm.validate()].every(
        x => x
      );
    },
  },
};
</script>
