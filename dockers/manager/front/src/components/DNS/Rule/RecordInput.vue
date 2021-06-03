<template>
  <div class="q-mb-md">
    <div class="text-h6">Records</div>
    <base-grid-input
      :titles="['Record', 'Enabled']"
      gridFormat="1fr auto"
      :entries="form"
      :error="error"
      @addEntry="addEntry"
      @removeEntry="removeEntry"
    >
      <template #inputs>
        <q-input
          class="col"
          flat
          v-model="model.content"
          @keypress.enter.prevent="addEntry"
          label="New record"
        />
        <div>
          <q-toggle
            v-model="model.enabled"
            title="Enabled"
            :color="model.enabled ? 'positive' : 'negative'"
          />

          <q-tooltip anchor="top middle" self="bottom middle">
            {{ model.enabled ? "Enabled" : "Disabled" }}
          </q-tooltip>
        </div>
      </template>
      <template #entry="{entry}">
        <div class="ellipsis">
          {{ entry.content }}
          <q-popup-edit v-model="entry.content">
            <q-input class="col" flat v-model="entry.content" label="Content" />
          </q-popup-edit>
        </div>
        <div class="ellipsis">
          <q-toggle
            v-model="entry.enabled"
            title="Enabled"
            :color="entry.enabled ? 'positive' : 'negative'"
          />

          <q-tooltip anchor="top middle" self="bottom middle">
            {{ entry.enabled ? "Enabled" : "Disabled" }}
          </q-tooltip>
        </div>
      </template>
    </base-grid-input>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";
export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  props: {
    label: { type: String, default: null }
  },
  data() {
    return { model: { content: null, enabled: true }, error: null };
  },
  formDefinition: [],
  methods: {
    validate(){
      if (this.form.length < 1){
        this.error = "You need at least one record."
        return false
      }
      return true
    },
    addEntry() {
      if (!this.model.content) return;
      this.form.unshift(this.model);
      this.model = { content: null, enabled: true };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
