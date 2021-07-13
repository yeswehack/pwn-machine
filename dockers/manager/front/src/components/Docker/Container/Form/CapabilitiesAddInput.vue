<template>
  <base-grid-input
    :readonly="readonly"
    :titles="['Added capabilities']"
    grid-format="1fr"
    :entries="form"
    @addEntry="addEntry"
    @removeEntry="removeEntry"
  >
    <template #inputs>
      <q-select
        v-model="model"
        :options="options"
        label="Add Capability"
        @input="addEntry"
      >
        <template #after>
          <help-link
            href="https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities"
          />
        </template>
      </q-select>
    </template>
  </base-grid-input>
</template>

<script>
import HelpLink from "src/components/HelpLink";
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { HelpLink, BaseGridInput },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: [],
  data() {
    const caps = [
      "AUDIT_CONTROL",
      "AUDIT_READ",
      "BLOCK_SUSPEND",
      "BPF",
      "CHECKPOINT_RESTORE",
      "DAC_READ_SEARCH",
      "IPC_LOCK",
      "IPC_OWNER",
      "LEASE",
      "LINUX_IMMUTABLE",
      "MAC_ADMIN",
      "MAC_OVERRIDE",
      "NET_ADMIN",
      "NET_BROADCAST",
      "PERFMON",
      "SYS_ADMIN",
      "SYS_BOOT",
      "SYS_MODULE",
      "SYS_NICE",
      "SYS_PACCT",
      "SYS_PTRACE",
      "SYS_RAWIO",
      "SYS_RESOURCE",
      "SYS_TIME",
      "SYS_TTY_CONFIG",
      "SYSLOG",
      "WAKE_ALARM"
    ];
    return { caps, model: null };
  },
  computed:{
    options() {
      return this.caps.filter(cap => !this.form.includes(cap))
    }
  },
  methods: {
    addEntry() {
      if (!this.model) {
        return;
      }
      this.form.unshift(this.model);
      this.model = null;
      this.validate();
    },
    validate() {
      return true;
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
      this.validate();
    }
  }
};
</script>
