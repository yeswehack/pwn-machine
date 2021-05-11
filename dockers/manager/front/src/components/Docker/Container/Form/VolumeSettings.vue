<template>
  <q-expansion-item
    expand-separator
    icon="eva-hard-drive-outline"
    label="Volumes"
    :caption="`${form.length} volume(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section class="q-px-sm">
        <div class="row q-col-gutter-sm full-width items-center">
          <div class="col col-2">
            <q-select
              flat
              :options="['volume', 'bind', 'tmpfs']"
              v-model="model.type"
              @keypress.enter.prevent="addEntry"
              label="Type"
            />
          </div>
          <div class="col col-4">
            <q-input
              flat
              v-model="model.name"
              @keypress.enter.prevent="addEntry"
              label="Name"
            />
          </div>
          <div class="col col-4">
            <q-input
              flat
              v-model="model.destination"
              @keypress.enter.prevent="addEntry"
              label="Destination"
            />
          </div>
          <div class="col ">
            <q-toggle v-model="model.mode" left-label />
          </div>
          <div class="col col-auto">
            <q-btn
              dense
              flat
              size="md"
              icon="eva-plus"
              color="positive"
              @click="addEntry"
              class="col col-auto"
            />
          </div>
        </div>
      </q-card-section>
      <q-card-section class="q-px-sm q-py-none">
        <div
          class="row q-col-gutter-sm full-width items-center"
          :key="idx"
          v-for="(entry, idx) of form"
        >
          <div class="col col-2">
            {{ entry.type }}
          </div>
          <div class="col col-4">
            {{ entry.name }}
          </div>
          <div class="col col-4">
            {{ entry.destination }}
          </div>
          <div class="col ">
            <q-toggle v-model="form[idx].mode" left-label />
          </div>
          <q-btn
            flat
            dense
            icon="eva-close"
            color="negative"
            size="md"
            class="col col-auto"
            @click="removeEntry(idx)"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <!--
  <EditTable
    :columns="columns"
    :createDefault="createVolume"
    v-model="formData"
  >
    <template #body-cell-type="props">
      <q-td>
        <q-select
          dense
          :options="['volume', 'bind', 'tmpfs']"
          v-model="props.row.type"
        />
      </q-td>
    </template>
    <template #body-cell-name="props">
      <q-td>
        <q-select
          dense
          :options="volumeNames"
          v-model="props.row.name"
          v-if="props.row.type == 'volume'"
        />
        <template v-else-if="props.row.type == 'bind'">
          {{ props.row.name }}
          <q-popup-edit v-model="props.row.name">
            <q-input v-model="props.row.name" dense autofocus />
          </q-popup-edit>
        </template>
        <div v-else class="disabled text-center">n/a</div>
      </q-td>
    </template>
    <template #body-cell-mode="props">
      <q-td auto-width><q-toggle dense size="sm" v-model="props.row.rw"/></q-td>
    </template>
  </EditTable>
  -->
</template>

<script>
import { shortName } from "src/utils";
import EditTable from "src/components/EditTable.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  formDefinition: [],
  components: {},
  data() {
    const model = { type: null, name: null, destination: null, mode: null };
    return {
      model
    };
  },
  methods: {
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = { type: null, name: null, destination: null, mode: null };
    }
  }
};
</script>
