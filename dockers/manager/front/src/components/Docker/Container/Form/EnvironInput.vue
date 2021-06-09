<template>
  <q-expansion-item
    icon="attach_money"
    label="Environment"
    :caption="`${form.length} variable(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <base-grid-input
          :readonly="readonly"
          :titles="['Name', 'Value']"
          grid-format="1fr 1fr"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
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
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.key }}
              <q-popup-edit v-model="entry.key">
                <q-input
                  v-model.number="entry.key"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.value }}
              <q-popup-edit v-model="entry.value">
                <q-input
                  v-model.number="entry.value"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
          </template>
        </base-grid-input>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  formDefinition: [],
  props: {
    label: { type: String, default: null },
    readonly: { type: Boolean, default: false }
  },
  data: () => ({ model: { key: "", value: "" } }),
  methods: {
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
