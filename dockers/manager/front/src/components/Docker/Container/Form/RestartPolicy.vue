<template>
  <div class="row items-center q-gutter-sm">
    <q-select
      class="col col-grow"
      filled
      clearable
      dense
      :options="options"
      v-model="formData"
      label="Restart policy"
    />

    <help-link
      href="https://docs.docker.com/engine/reference/run/#restart-policies---restart"
    />
  </div>
</template>

<script>
import HelpLink from "src/components/HelpLink";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: { HelpLink },
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
    return { options };
  }
};
</script>

<style></style>
