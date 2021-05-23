<template>
  <div class="q-mb-md">
    <label class="row text-bold">Mirrors</label>
    <div class="row q-gutter-sm">
      <q-select
        class="col"
        flat
        v-model="name"
        @keypress.enter.prevent="addEntry"
        :options="services"
        label="Service"
      />
      <q-input
        class="col"
        type="number"
        flat
        v-model.number="percent"
        @keypress.enter.prevent="addEntry"
        label="Percent"
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
            <div class="col col-6">
              {{ entry.name }}
              <q-popup-edit v-model="form[idx].name">
                <q-select
                  flat
                  v-model="form[idx].name"
                  @keypress.enter.prevent="addEntry"
                  :options="services"
                />
              </q-popup-edit>
            </div>
            <div class="col ">
              {{ entry.percent }}

              <q-popup-edit v-model="form[idx].percent">
                <q-input v-model.number="form[idx].percent" dense autofocus />
              </q-popup-edit>
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
    <label class="row text-negative" v-if="errorMsg">{{ errorMsg }}</label>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    services: { type: Array, default: () => [] },
    label: { type: String, default: null }
  },
  data() {
    return { name: null, percent: null, errorMsg: "" };
  },
  formDefinition: [],
  methods: {
    addEntry() {
      if (!this.name || [null, undefined, ""].includes(this.percent)) return
      this.form.unshift({ name: this.name, percent: this.percent });
      this.name = null;
      this.percent = null;
      this.validate();
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
      this.validate();
    },
    validate() {
      this.errorMsg = "";
      if (!Array.isArray(this.form) || this.form.length == 0) {
        this.errorMsg = "You must choose at least one service";
        return false;
      }
      return true;
    }
  }
};
</script>
