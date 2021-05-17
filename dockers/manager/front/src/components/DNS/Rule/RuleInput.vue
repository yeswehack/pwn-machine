<template>
  <div class="q-mb-md">
    <label class="row text-bold">Headers</label>
    <div class="row q-gutter-sm">
      <q-input
        class="col"
        flat
        v-model="model"
        @keypress.enter.prevent="addEntry"
        label="Name"
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
                <q-input v-model.number="form[idx].content" dense autofocus />
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
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    label: { type: String, default: null }
  },
  data() {
    return { model: null };
  },
  formDefinition: [],
  methods: {
    addEntry() {
      this.form.unshift({ content: this.model, enabled: true });
      this.model = null;
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
