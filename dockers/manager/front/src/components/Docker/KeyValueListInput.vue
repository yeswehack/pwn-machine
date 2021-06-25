<template>
  <q-expansion-item v-bind="$attrs">
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
              ref="key"
              v-model="model.key"
              :rules="[required('Name cannot be empty')]"
              lazy-rules="ondemand"
              class="col"
              flat
              label="Name"
              @input="$refs.key.resetValidation()"
              @keypress.enter.prevent="addEntry"
            />
            <q-input
              v-model="model.value"
              class="col fit"
              flat
              label="Value"
              @keypress.enter.prevent="addEntry"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.key }}
              <q-popup-edit
                v-model="entry.key"
                :validate="required('Name cannot be empty')"
              >
                <template #default="{validate}">
                  <q-input
                    v-model="entry.key"
                    :rules="[validate]"
                    :readonly="readonly"
                    dense
                    autofocus
                  />
                </template>
              </q-popup-edit>
            </div>
            <div class="ellipsis fit">
              {{ entry.value }}
              <q-popup-edit v-model="entry.value">
                <q-input
                  v-model="entry.value"
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
    readonly: { type: Boolean, default: false }
  },
  data: () => ({ model: { key: "", value: "" } }),
  methods: {
    addEntry() {
      if (this.$refs.key.validate()) {
        this.form.unshift(this.model);
        this.model = { key: "", value: "" };
        this.$refs.key.resetValidation();
      }
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
