<template>
  <div>
    <div class="text-h6">Weighted services</div>
    <base-grid-input
      :readonly="readonly"
      :titles="['Service', 'Weight']"
      gridFormat="1fr 1fr"
      :entries="form"
      :error="errorMsg"
      @addEntry="addEntry"
      @removeEntry="removeEntry"
    >
      <template #inputs>
        <q-select
          flat
          v-model="model.name"
          @keypress.enter.prevent="addEntry"
          :options="serviceOptions"
          label="Service"
        />
        <q-input
          type="number"
          flat
          v-model.number="model.weight"
          @keypress.enter.prevent="addEntry"
          label="Weight"
        />
      </template>
      <template #entry="{entry}">
        <div class="ellipsis">
          {{ entry.name }}
          <q-popup-edit v-model="entry.name">
            <q-select
              class="col"
              flat
              v-model="entry.name"
              @keypress.enter.prevent="addEntry"
              :options="serviceOptions"
            />
          </q-popup-edit>
        </div>
        <div class="ellipsis">
          {{ entry.weight }}
          <q-popup-edit v-model="entry.weight">
            <q-input
              class="col"
              flat
              v-model.number="entry.weight"
              @keypress.enter.prevent="addEntry"
            />
          </q-popup-edit>
        </div>
      </template>
    </base-grid-input>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false },
    protocol: { type: String, default: null },
    label: { type: String, default: null }
  },
  formDefinition: [],
  apollo: {
    services: {
      query: api.traefik.services.LIST_SERVICES,
      variables() {
        return { protocols: [this.protocol] };
      },
      update: data => data.traefikServices
    }
  },
  computed: {
    serviceOptions() {
      return (this.services ?? []).map(s => s.name);
    }
  },
  data: () => ({ model: { name: null, weight: null }, errorMsg: "" }),
  methods: {
    addEntry() {
      if (!this.model.name || !Number.isFinite(this.model.weight)) return;
      this.form.unshift(this.model);
      this.model = { name: null, weight: null };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    validate() {
      this.errorMsg = "";
      if (!Array.isArray(this.form) || this.form.length === 0) {
        this.errorMsg = "You must choose at least one service";
        return false;
      }
      return true;
    }
  }
};
</script>
