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
          gridFormat="3fr 2fr  6fr"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-input
              label="Container port"
              @keypress.enter.prevent="addEntry"
              v-model.number="model.containerPort"
              @input="addPort"
            />
            <q-select
              label="Protocol"
              :options="['tcp', 'udp']"
              v-model="model.protocol"
            />
            <q-select
              use-chips
              new-value-mode="add"
              use-input
              hide-dropdown-icon
              multiple
              label="Targets"
              v-model="model.targets"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.containerPort }}

              <q-popup-edit v-model="entry.containerPort">
                <q-input
                  :readonly="readonly"
                  label="Container port"
                  v-model.number="entry.containerPort"
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.protocol }}
              <q-popup-edit v-model="entry.protocol">
                <q-select
                  :readonly="readonly"
                  label="Protocol"
                  :options="['tcp', 'udp']"
                  v-model="entry.protocol"
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.targets ? entry.targets.join(", ") : "Not forwarded" }}

              <q-popup-edit v-model="entry.targets">
                <q-select
                  :readonly="readonly"
                  use-chips
                  new-value-mode="add"
                  use-input
                  hide-dropdown-icon
                  multiple
                  label="Targets"
                  v-model="entry.targets"
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
  props: {
    readonly: { type: Boolean, default: false },
    container: { type: Object, default: null }
  },
  mixins: [DeepForm],
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
