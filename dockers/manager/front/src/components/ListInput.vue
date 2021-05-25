<template>
  <base-grid-input
    :readonly="readonly"
    :titles="[label]"
    gridFormat="1fr"
    :entries="form"
    @addEntry="addEntry"
    @removeEntry="removeEntry"
    :error="errorMsg"
  >
    <template #inputs>
      <q-input
        v-bind="$attrs"
        flat
        v-model="model"
        @keypress.enter.prevent="addEntry"
        :label="label"
      />
    </template>
    <template #entry="props">
      <div class="ellipsis">
        {{ props.entry }}
        <q-popup-edit v-model="props.entry">
          <q-input v-model="props.entry" dense autofocus />
        </q-popup-edit>
      </div>
    </template>
  </base-grid-input>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  props: {
    rules: { type: Array, default: () => [] },
    readonly: { type: Boolean, default: false },
    label: { type: String, default: null }
  },
  data() {
    return { model: "", errorMsg: null };
  },
  formDefinition: [],
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
      this.errorMsg = "";
      for (const rule of this.rules) {
        const msg = rule(this.form);
        if (msg) {
          this.errorMsg = msg;
          return false;
        }
      }
      return true;
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
      this.validate();
    }
  }
};
</script>
