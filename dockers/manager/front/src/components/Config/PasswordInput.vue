<template>
  <div>
    <q-input
      ref="new"
      label="New password"
      type="password"
      :rules="[required('Please enter a password')]"
      v-model="form"
    />
    <q-input
      ref="confirm"
      label="Confirm password"
      type="password"
      :rules="[matchesNew]"
      reactive-rules
      v-model="repeated"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  formDefinition: "",
  data: () => ({ repeated: "" }),
  watch: {
    form() {
      this.repeated = "";
    }
  },
  methods: {
    matchesNew(v) {
      return v === this.form || "Passwords don't match";
    }
  }
};
</script>
