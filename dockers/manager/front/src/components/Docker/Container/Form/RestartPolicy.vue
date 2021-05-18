<template>
  <q-select
    v-bind="$attrs"
    clearable
    :options="options"
    v-model="model"
    label="Restart policy"
    @input="input"
  >
    <template #after>
      <help-link
        href="https://docs.docker.com/engine/reference/run/#restart-policies---restart"
      />
    </template>
  </q-select>
</template>

<script>
import HelpLink from "src/components/HelpLink";
export default {
  components: { HelpLink },
  props: { value: { type: String, default: null } },
  data() {
    const options = [
      {
        label: "Don't restart",
        value: "no-restart"
      },
      {
        label: "Always",
        value: "always"
      },
      {
        label: "Unless stopped",
        value: "unless-stopped"
      },
      {
        label: "On failure",
        value: "on-failure"
      }
    ];
    return { options, model: this.value };
  },
  methods: {
    input(v) {
      this.$emit("input", v?.value ?? null);
    }
  }
};
</script>

<style></style>
