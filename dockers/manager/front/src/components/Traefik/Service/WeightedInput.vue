<template>
  <div class="q-mb-md">
    <label class="row text-bold">Weighted Round Robin</label>
    <div class="row q-gutter-sm">
      <q-select
        class="col"
        flat
        v-model="model.name"
        @keypress.enter.prevent="addEntry"
        :options="serviceOptions"
        label="Service"
      />
      <q-input
        class="col"
        type="number"
        flat
        v-model.number="model.weight"
        @keypress.enter.prevent="addEntry"
        label="Weight"
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
                  class="col"
                  flat
                  v-model="form[idx].name"
                  @keypress.enter.prevent="addEntry"
                  :options="serviceOptions"
                />
              </q-popup-edit>
            </div>
            <div class="col ">
              {{ entry.weight }}

              <q-popup-edit v-model="form[idx].weight">
                <q-input v-model.number="form[idx].weight" dense autofocus />
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
  </div>
</template>

<script>
import gql from "graphql-tag"
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    protocol: { type: String, default: null },
    label: { type: String, default: null }
  },
  formDefinition: [],
  apollo: {
    services: {
      query: gql`
        query getServices($protocols: [TraefikProtocol!]) {
          traefikServices(protocols: $protocols) {
            name
          }
        }
      `,
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
  data() {
    return { model: { name: "", weight: "" } };
  },
  methods: {
    addEntry() {
      this.form.unshift(this.model);
      this.model = { name: null, weight: null };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
