<template>
  <div class="q-mb-md">
    <div class="text-h6">Records</div>
    <base-grid-input
      :titles="['Record', 'Enabled']"
      gridFormat="1fr auto"
      :entries="form"
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
    <div v-if="0">
      <label class="row text-bold">Records</label>
      <div class="row q-gutter-sm">
        <q-input
          class="col"
          flat
          v-model="model"
          @keypress.enter.prevent="addEntry"
          label="Content"
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
              <div class="col  ellipsis">
                {{ entry.content }}
                <q-popup-edit v-model="form[idx].content">
                  <q-input v-model="form[idx].content" dense autofocus />
                </q-popup-edit>
              </div>
              <div class="col col-auto">
                <q-toggle
                  dense
                  v-model="form[idx].enabled"
                  title="Enabled"
                  :color="form[idx].enabled ? 'positive' : 'negative'"
                />
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
    return { model: { content: null, enabled: true } };
  },
  formDefinition: [],
  methods: {
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
