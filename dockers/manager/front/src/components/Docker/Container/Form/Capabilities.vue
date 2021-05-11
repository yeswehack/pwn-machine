<template>
  <div class="row items-center">
    <q-select
      class="col col-grow"
      use-chips
      multiple
      clearable
      :options="options"
      v-model="model"
      @input="input"
      label="Capabilities"
    />
    <help-link
      class="q-ml-md"
      href="https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities"
    />
  </div>
</template>

<script>
import HelpLink from "src/components/HelpLink";
export default {
  props: { value: { type: String, default: null } },
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
    return { options, model: this.value };
  },
  methods: {
    input(v) {
      this.$emit("input", v ?? null);
    }
  }
};
</script>

<style></style>
