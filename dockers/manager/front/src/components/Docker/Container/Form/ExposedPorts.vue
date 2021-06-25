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
          grid-format="150px 85px auto"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-input
              ref="port"
              v-model.number="model.containerPort"
              mask="#####"
              :rules="[validatePort]"
              lazy-rules="ondemand"
              label="Container port"
              @input="$refs.port.resetValidation()"
              @keypress.enter.prevent="addEntry"
              @change="addPort(model.containerPort)"
            />
            <q-select
              v-model="model.protocol"
              class="fit"
              label="Protocol"
              :options="['tcp', 'udp']"
            />
            <q-select
              v-model="model.targets"
              class="fit"
              use-chips
              new-value-mode="add"
              use-input
              hide-dropdown-icon
              multiple
              outlined
              label="Targets"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.containerPort }}

              <q-popup-edit
                v-model="entry.containerPort"
                :validate="validatePort"
              >
                <template #default="{validate}">
                  <q-input
                    v-model.number="entry.containerPort"
                    mask="#####"
                    :rules="[validate]"
                    :readonly="readonly"
                    dense
                    autofocus
                  />
                </template>
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.protocol }}
              <q-popup-edit v-model="entry.protocol" :validate="required()">
                <q-select
                  v-model="entry.protocol"
                  :readonly="readonly"
                  :options="['tcp', 'udp']"
                  dense
                  autofocus
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
                  outlined
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
  data: () => ({ model: { ...defaultModel } }),
  methods: {
    validatePort(p) {
      const max = 2 ** 16 - 1;
      return (
        (Number.isInteger(p) && p >= 0 && p <= max) ||
        `Must be in range 0 - ${max}`
      );
    },
    addPort(port) {
      this.model.targets = port ? [`0.0.0.0:${port}`] : [];
    },
    addEntry() {
      if (!this.model.protocol) return;
      if (this.$refs.port.validate()) {
        this.form.unshift(this.model);
        this.model = { ...defaultModel };
      }
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
