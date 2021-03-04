<template>
  <div class="row items-center q-gutter-sm">
    <q-select
      class="col col-grow"
      filled
      use-chips
      multiple
      clearable
      dense
      :options="options"
      v-model="formData"
      label="Capabilities"
    />
    <help-link
      href="https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities"
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
      "AUDIT_WRITE",
      "CHOWN",
      "DAC_OVERRIDE",
      "FOWNER",
      "FSETID",
      "KILL",
      "MKNOD",
      "NET_BIND_SERVICE",
      "NET_RAW",
      "SETFCAP",
      "SETGID",
      "SETPCAP",
      "SETUID",
      "SYS_CHROOT"
    ];
    return { options };
  }
};
</script>

<style></style>
