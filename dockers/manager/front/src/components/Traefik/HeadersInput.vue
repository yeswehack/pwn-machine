<template>
  <div class="q-mb-md">
    <label class="row text-bold">{{ label }}</label>
    <div class="row q-gutter-sm">
      <q-input
        v-model="model.key"
        class="col"
        flat
        label="Name"
        @keypress.enter.prevent="addEntry"
      />
      <q-input
        v-model="model.value"
        class="col"
        flat
        label="Value"
        @keypress.enter.prevent="addEntry"
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
    </div>
    <q-list separator dense padding>
      <q-item v-for="(entry, idx) of form" :key="idx">
        <q-item-section>
          <div class="row q-col-gutter-sm">
            <div class="col col-6">
              {{ entry.key }}
              <q-popup-edit v-model="form[idx].key">
                <q-input v-model.number="form[idx].key" dense autofocus />
              </q-popup-edit>
            </div>
            <div class="col ">
              {{ entry.value }}

              <q-popup-edit v-model="form[idx].value">
                <q-input v-model.number="form[idx].value" dense autofocus />
              </q-popup-edit>
            </div>
            <div class="col col-auto">
              <q-btn
                flat
                dense
                icon="eva-close"
                color="negative"
                size="sm"
                @click="removeEntry(idx)"
              />
            </div>
          </div>
        </q-item-section>
      </q-item>
      <q-item v-if="form.length === 0">
        <q-item-section>
          ...
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    label: { type: String, default: "Headers" }
  },
  data: () => ({ model: { key: "", value: "" } }),
  formDefinition: [],
  methods: {
    addEntry() {
      if (!this.model?.key) return;
      this.form.unshift(this.model);
      this.model = { key: "", value: "" };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
