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
          gridFormat="1fr 1fr"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
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
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.key }}
              <q-popup-edit v-model="entry.key">
                <q-input
                  :readonly="readonly"
                  v-model.number="entry.key"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.value }}
              <q-popup-edit v-model="entry.value">
                <q-input
                  :readonly="readonly"
                  v-model.number="entry.value"
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
  data() {
    return { model: { key: "", value: "" } };
  },
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
