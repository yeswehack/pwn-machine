<template>
  <base-grid-input
    :readonly="readonly"
    :titles="[label]"
    grid-format="1fr"
    :entries="form"
    :error="errorMsg"
    @addEntry="addEntry"
    @removeEntry="removeEntry"
  >
    <template #inputs>
      <q-input
        v-model="model"
        v-bind="$attrs"
        flat
        :label="label"
        @keypress.enter.prevent="addEntry"
      />
    </template>
    <template #entry="props">
      <div v-if="objectKey" class="ellipsis">
        {{ props.entry[objectKey] }}
        <q-popup-edit v-model="props.entry[objectKey]">
          <q-input v-model="props.entry[objectKey]" dense autofocus />
        </q-popup-edit>
      </div>
      <div v-else class="ellipsis">
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
    objectKey: { type: String, default: null },
    rules: { type: Array, default: () => [] },
    readonly: { type: Boolean, default: false },
    label: { type: String, default: null }
  },
  data: () => ({ model: "", errorMsg: null }),
  formDefinition: [],
  methods: {
    addEntry() {
      if (!this.model) {
        return;
      }
      if (this.objectKey) {
        this.form.unshift({ [this.objectKey]: this.model });
      } else {
        this.form.unshift(this.model);
      }
      this.model = null;
      this.validate();
    },
    validate() {
      this.errorMsg = "";
      for (const rule of this.rules) {
        const msg = rule(this.form);
        if (typeof msg === "string") {
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