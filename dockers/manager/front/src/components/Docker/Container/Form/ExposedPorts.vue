<template>
  <q-expansion-item
    icon="cable"
    label="Exposed ports"
    :caption="`${form.length} port(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <base-grid-input
          :readonly="readonly"
          :titles="['Container port', 'Protocol', 'Targets']"
          grid-format="3fr 2fr  6fr"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-input
              v-model.number="model.containerPort"
              label="Container port"
              @keypress.enter.prevent="addEntry"
              @input="addPort"
            />
            <q-select
              v-model="model.protocol"
              label="Protocol"
              :options="['tcp', 'udp']"
            />
            <q-select
              v-model="model.targets"
              use-chips
              new-value-mode="add"
              use-input
              hide-dropdown-icon
              multiple
              label="Targets"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.containerPort }}

              <q-popup-edit v-model="entry.containerPort">
                <q-input
                  v-model.number="entry.containerPort"
                  :readonly="readonly"
                  label="Container port"
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.protocol }}
              <q-popup-edit v-model="entry.protocol">
                <q-select
                  v-model="entry.protocol"
                  :readonly="readonly"
                  label="Protocol"
                  :options="['tcp', 'udp']"
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.targets ? entry.targets.join(", ") : "Not forwarded" }}

              <q-popup-edit v-model="entry.targets">
                <q-select
                  v-model="entry.targets"
                  :readonly="readonly"
                  use-chips
                  new-value-mode="add"
                  use-input
                  hide-dropdown-icon
                  multiple
                  label="Targets"
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
import DeepForm from "src/mixins/DeepForm.js";
import BaseGridInput from "src/components/BaseGridInput.vue";

const defaultModel = {
  containerPort: null,
  protocol: "tcp",
  targets: []
};

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false },
    container: { type: Object, default: null }
  },
  formDefinition: [],
  data: () => ({ model: defaultModel }),
  methods: {
    addPort(port) {
      this.model.targets = [`0.0.0.0:${port}`];
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = defaultModel;
    }
  }
};
</script>
