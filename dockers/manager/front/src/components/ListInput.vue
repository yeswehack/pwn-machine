<template>
  <div class="list-inputq-mb-md">
    <q-input
      v-bind="$attrs"
      flat
      v-model="model"
      @keypress.enter.prevent="addEntry"
      :label="label"
    >
      <template #append>
        <q-btn
          dense
          flat
          size="md"
          icon="eva-plus"
          color="positive"
          @click="addEntry"
        />
      </template>
    </q-input>
    <q-list separator dense padding>
      <q-item :key="idx" v-for="(entry, idx) of form">
        <q-item-section v-if="objectKey">
          {{ entry[objectKey] }}
          <q-popup-edit v-model="form[idx][objectKey]">
            <q-input v-model="form[idx][objectKey]" dense autofocus />
          </q-popup-edit>
        </q-item-section>
        <q-item-section v-else>
          {{ entry }}
          <q-popup-edit v-model="form[idx]">
            <q-input v-model="form[idx]" dense autofocus />
          </q-popup-edit>
        </q-item-section>
        <q-item-section avatar>
          <q-btn
            flat
            dense
            icon="eva-close"
            color="negative"
            size="sm"
            @click="removeEntry(idx)"
          />
        </q-item-section>
      </q-item>
      <q-item v-if="form.length == 0">
        <q-item-section>...</q-item-section>
      </q-item>
    </q-list>
    <label class="row text-negative" v-if="errorMsg">{{ errorMsg }}</label>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    rules: { type: Array, default: () => [] },
    objectKey: { type: String, default: null },
    label: { type: String, default: null }
  },
  data() {
    return { model: "", errorMsg: "" };
  },
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
