<template>
  <base-grid-input
    :readonly="readonly"
    :titles="['Dropped capabilities']"
    grid-format="1fr"
    :entries="form"
    @addEntry="addEntry"
    @removeEntry="removeEntry"
  >
    <template #inputs>
      <q-select
        v-model="model"
        :options="options"
        label="Drop Capability"
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
