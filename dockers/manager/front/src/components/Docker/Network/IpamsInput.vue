<template>
  <q-expansion-item expand-separator :caption="caption">
    <template #header>
      <q-item-section avatar>
        <q-avatar icon="eva-share-outline" />
      </q-item-section>
      <q-item-section>
        <q-item-label>
          IPAM Settings
        </q-item-label>
        <q-item-label caption>
          {{ caption }}
        </q-item-label>
      </q-item-section>
      <q-item-section side>
        <help-link
          href="https://docs.docker.com/engine/reference/commandline/network_create/#bridge-driver-options"
        />
      </q-item-section>
    </template>
    <q-separator />
    <q-card>
      <q-card-section>
        <base-grid-input
          :readonly="readonly"
          :titles="['Subnet', 'Gateway', 'IP Range']"
          grid-format="1fr 1fr 1fr"
          :entries="form"
          @addEntry="addEntry"
          @removeEntry="removeEntry"
        >
          <template #inputs>
            <q-input
              v-model="model.subnet"
              class="col"
              flat
              label="Subnet"
              @keypress.enter.prevent="addEntry"
            />
            <q-input
              v-model="model.gateway"
              class="col"
              flat
              label="Gateway"
              @keypress.enter.prevent="addEntry"
            />
            <q-input
              v-model="model.ipRange"
              class="col"
              flat
              label="IP Range"
              @keypress.enter.prevent="addEntry"
            />
          </template>
          <template #entry="{entry}">
            <div class="ellipsis">
              {{ entry.subnet }}
              <q-popup-edit v-model="entry.subnet">
                <q-input
                  v-model.number="entry.subnet"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.gateway }}
              <q-popup-edit v-model="entry.gateway">
                <q-input
                  v-model.number="entry.gateway"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-popup-edit>
            </div>
            <div class="ellipsis">
              {{ entry.ipRange }}
              <q-popup-edit v-model="entry.ipRange">
                <q-input
                  v-model.number="entry.ipRange"
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
import HelpLink from "src/components/HelpLink.vue";
import BaseGridInput from "src/components/BaseGridInput.vue";

const defaultModel = {
  subnet: null,
  gateway: null,
  ipRange: null
};

export default {
  components: { HelpLink, BaseGridInput },
  mixins: [DeepForm],
  props: { readonly: { type: Boolean, default: false } },
  formDefinition: [],
  data: () => ({ model: defaultModel }),
  computed: {
    caption() {
      if (this.form.length === 0) {
        return "Automatic";
      }
      return `${this.form.length} setting(s)`;
    }
  },
  methods: {
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    addEntry() {
      if (!this.model.subnet) return;
      this.form.unshift(this.model);
      this.model = defaultModel;
    }
  }
};
</script>
