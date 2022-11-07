<template>
  <div>
    <q-input
      ref="new"
      v-model="form"
      label="New password"
      type="password"
      :rules="[required('Please enter a password')]"
    />
    <q-input
      ref="confirm"
      v-model="repeated"
      label="Confirm password"
      type="password"
      :rules="[matchesNew]"
      reactive-rules
      lazy-rules
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
