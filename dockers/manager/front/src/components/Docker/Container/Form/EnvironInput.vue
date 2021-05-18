<template>
  <q-expansion-item
    icon="attach_money"
    label="Environment"
    :caption="`${form.length} variable(s)`"
  >
    <q-card>
      <q-separator />
      <q-card-section>
        <div class="row" v-if="!readonly">
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
          <q-item v-if="readonly">
            <q-item-section>
              <div class="row q-col-gutter-sm">
                <div class="col col-6 text-bold">Name</div>
                <div class="col col-6 text-bold">Value</div>
              </div>
            </q-item-section>
          </q-item>
          <q-item :key="idx" v-for="(entry, idx) of form">
            <q-item-section>
              <div class="row q-col-gutter-sm">
                <div class="col col-6 ellipsis">
                  {{ entry.key }}
                  <q-popup-edit v-model="form[idx].key" v-if="!readonly">
                    <q-input v-model.number="form[idx].key" dense autofocus />
                  </q-popup-edit>
                </div>
                <div class="col ellipsis">
                  {{ entry.value }}

                  <q-popup-edit v-model="form[idx].value" v-if="!readonly">
                    <q-input v-model.number="form[idx].value" dense autofocus />
                  </q-popup-edit>
                </div>
                <div class="col col-auto">
                  <q-btn
                    v-if="!readonly"
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
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
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
