<template>
  <div class="q-mb-md">
    <label class="row text-bold">Headers</label>
    <div class="row q-gutter-sm">
      <q-input
        class="col"
        flat
        v-model="model.key"
        @keypress.enter.prevent="addEntry"
        label="Name"
      />
      <q-input
        class="col"
        flat
        v-model="model.value"
        @keypress.enter.prevent="addEntry"
        label="Value"
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
      <q-item :key="idx" v-for="(entry, idx) of form">
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
      <q-item v-if="form.length == 0">
        <q-item-section>
          ...
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import deepcopy from "deepcopy";

export default {
  mixins: [DeepForm],
  props: {
    label: { type: String, default: null }
  },
  data() {
    return { model: { key: "", value: "" } };
  },
  methods: {
    createDefaultForm(v) {
      const form = v ? deepcopy(v) : [];
      return form;
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = { key: "", value: "" };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
